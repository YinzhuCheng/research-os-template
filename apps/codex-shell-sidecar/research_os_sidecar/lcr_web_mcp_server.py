from __future__ import annotations

import html
import ipaddress
import json
import base64
import os
import re
import socket
import sys
import traceback
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, BinaryIO


SERVER_NAME = "lcr-web-tools"
SERVER_VERSION = "0.1.0"
DEFAULT_TIMEOUT_SEC = 20
DEFAULT_MAX_CHARS = 6000
DEFAULT_BATCH_MAX_QUERIES = 8
DEFAULT_RESEARCH_FETCH_TOP_N = 6
_OUTPUT_FRAMING = "header"


def main() -> None:
    _debug("started", argv=sys.argv[:3])
    while True:
        message = _read_message(sys.stdin.buffer)
        if message is None:
            _debug("eof")
            break
        response = _handle_message(message)
        if response is not None:
            _write_message(sys.stdout.buffer, response)


def _handle_message(message: dict[str, Any]) -> dict[str, Any] | None:
    request_id = message.get("id")
    method = str(message.get("method") or "")
    params = message.get("params") or {}
    try:
        if method == "initialize":
            return _result(
                request_id,
                {
                    "protocolVersion": str(params.get("protocolVersion") or "2024-11-05"),
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                    "instructions": (
                        "Use LCR web tools for batch source lookup and lightweight research briefs. "
                        "Return URLs with claims. Do not pass secrets, Authorization headers, cookies, or API keys."
                    ),
                },
            )
        if method in {"notifications/initialized", "initialized"}:
            return None
        if method == "tools/list":
            return _result(request_id, {"tools": _tools()})
        if method == "resources/list":
            return _result(request_id, {"resources": []})
        if method == "resources/templates/list":
            return _result(request_id, {"resourceTemplates": []})
        if method == "tools/call":
            return _result(request_id, _call_tool(params))
        if request_id is None:
            return None
        return _error(request_id, -32601, f"Unsupported method: {method}")
    except Exception as exc:  # noqa: BLE001
        details = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        _debug("handler_error", method=method, error=details[:500])
        return _error(request_id, -32000, details)


def _tools() -> list[dict[str, Any]]:
    return [
        {
            "name": "lcr_web_search_batch",
            "description": (
                "Run one or more public web searches and return a deduplicated result set. A single basic "
                "search is represented as queries=[{query: ...}]. Use this before claiming current facts, "
                "design references, tool installation guidance, or source-backed recommendations."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "queries": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": DEFAULT_BATCH_MAX_QUERIES,
                        "items": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query."},
                                "max_results": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
                            },
                            "required": ["query"],
                            "additionalProperties": False,
                        },
                    },
                    "dedupe": {"type": "boolean", "default": True, "description": "Merge duplicate URLs across queries."},
                    "timeout_sec": {"type": "integer", "minimum": 5, "maximum": 60, "default": DEFAULT_TIMEOUT_SEC},
                },
                "required": ["queries"],
                "additionalProperties": False,
            },
        },
        {
            "name": "lcr_web_research_brief",
            "description": (
                "Build a lightweight research brief from a goal: run multiple searches, fetch top public pages, "
                "redact/truncate page text, and return sources, excerpts, unresolved questions, and suggested "
                "follow-up queries. Use for multi-step web research instead of manual one-by-one searching."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "research_goal": {"type": "string", "description": "What to investigate and why."},
                    "queries": {
                        "type": "array",
                        "maxItems": DEFAULT_BATCH_MAX_QUERIES,
                        "items": {"type": "string"},
                        "description": "Optional explicit search queries. If omitted, the tool derives a small query plan from research_goal.",
                    },
                    "source_urls": {
                        "type": "array",
                        "maxItems": 10,
                        "items": {"type": "string"},
                        "description": "Optional known public URLs to fetch alongside search results.",
                    },
                    "search_top_k": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
                    "fetch_top_n": {"type": "integer", "minimum": 1, "maximum": 12, "default": DEFAULT_RESEARCH_FETCH_TOP_N},
                    "max_chars_per_source": {"type": "integer", "minimum": 500, "maximum": 10000, "default": 3000},
                    "timeout_sec": {"type": "integer", "minimum": 5, "maximum": 60, "default": DEFAULT_TIMEOUT_SEC},
                },
                "required": ["research_goal"],
                "additionalProperties": False,
            },
        },
        {
            "name": "lcr_web_search",
            "description": "Compatibility alias for lcr_web_search_batch with one query. Prefer lcr_web_search_batch.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query."},
                    "max_results": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
                    "timeout_sec": {"type": "integer", "minimum": 5, "maximum": 60, "default": DEFAULT_TIMEOUT_SEC},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
        {
            "name": "lcr_web_fetch",
            "description": "Compatibility low-level public HTTP(S) fetch. Prefer lcr_web_research_brief for agent research.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Public HTTP(S) URL to fetch."},
                    "max_chars": {"type": "integer", "minimum": 500, "maximum": 20000, "default": DEFAULT_MAX_CHARS},
                    "timeout_sec": {"type": "integer", "minimum": 5, "maximum": 60, "default": DEFAULT_TIMEOUT_SEC},
                },
                "required": ["url"],
                "additionalProperties": False,
            },
        },
    ]


def _call_tool(params: dict[str, Any]) -> dict[str, Any]:
    name = str(params.get("name") or "")
    args = params.get("arguments") or {}
    if not isinstance(args, dict):
        raise ValueError("Tool arguments must be an object.")
    if name == "lcr_web_search_batch":
        payload = _search_batch(
            args.get("queries"),
            dedupe=bool(args.get("dedupe", True)),
            timeout_sec=int(args.get("timeout_sec") or DEFAULT_TIMEOUT_SEC),
        )
        return _tool_text(payload)
    if name == "lcr_web_research_brief":
        payload = _research_brief(
            research_goal=str(args.get("research_goal") or "").strip(),
            queries=args.get("queries"),
            source_urls=args.get("source_urls"),
            search_top_k=int(args.get("search_top_k") or 5),
            fetch_top_n=int(args.get("fetch_top_n") or DEFAULT_RESEARCH_FETCH_TOP_N),
            max_chars_per_source=int(args.get("max_chars_per_source") or 3000),
            timeout_sec=int(args.get("timeout_sec") or DEFAULT_TIMEOUT_SEC),
        )
        return _tool_text(payload)
    if name == "lcr_web_search":
        query = str(args.get("query") or "").strip()
        if not query:
            raise ValueError("query is required.")
        payload = _search_batch(
            [{"query": query, "max_results": int(args.get("max_results") or 5)}],
            dedupe=True,
            timeout_sec=int(args.get("timeout_sec") or DEFAULT_TIMEOUT_SEC),
        )
        payload["tool"] = "lcr_web_search"
        return _tool_text(payload)
    if name == "lcr_web_fetch":
        url = str(args.get("url") or "").strip()
        if not url:
            raise ValueError("url is required.")
        payload = _fetch(url, max_chars=int(args.get("max_chars") or DEFAULT_MAX_CHARS), timeout_sec=int(args.get("timeout_sec") or DEFAULT_TIMEOUT_SEC))
        return _tool_text(payload)
    raise ValueError(f"Unknown LCR web tool: {name}")


def _search_batch(queries: Any, *, dedupe: bool, timeout_sec: int) -> dict[str, Any]:
    query_specs = _normalize_query_specs(queries)
    results_by_query = []
    merged: list[dict[str, str]] = []
    warnings: list[str] = []
    for spec in query_specs:
        query = spec["query"]
        result = _search(query, max_results=spec["max_results"], timeout_sec=timeout_sec)
        results = [dict(item) for item in list(result.get("results") or []) if isinstance(item, dict)]
        results_by_query.append(
            {
                "query": query,
                "result_count": len(results),
                "results": results,
                "warning": result.get("warning") or "",
            }
        )
        if result.get("warning"):
            warnings.append(f"{query}: {result.get('warning')}")
        merged.extend({**item, "query": query} for item in results)
    if dedupe:
        merged = _dedupe_results(merged)
    return {
        "tool": "lcr_web_search_batch",
        "source": "duckduckgo_html",
        "query_count": len(query_specs),
        "result_count": len(merged),
        "results_by_query": results_by_query,
        "merged_results": merged,
        "warnings": warnings,
        "note": "Basic search is queries=[{query: ...}]. Use lcr_web_research_brief when page fetching and a source pack are needed.",
    }


def _research_brief(
    *,
    research_goal: str,
    queries: Any,
    source_urls: Any,
    search_top_k: int,
    fetch_top_n: int,
    max_chars_per_source: int,
    timeout_sec: int,
) -> dict[str, Any]:
    if not research_goal:
        raise ValueError("research_goal is required.")
    explicit_queries = _string_list(queries)
    query_texts = explicit_queries or _derive_research_queries(research_goal)
    query_specs = [{"query": query, "max_results": max(1, min(10, search_top_k))} for query in query_texts[:DEFAULT_BATCH_MAX_QUERIES]]
    search_payload = _search_batch(query_specs, dedupe=True, timeout_sec=timeout_sec)
    candidates: list[dict[str, str]] = []
    for url in _string_list(source_urls)[:10]:
        candidates.append({"title": "", "url": url, "snippet": "User-provided source URL.", "query": "source_urls"})
    candidates.extend([dict(item) for item in list(search_payload.get("merged_results") or []) if isinstance(item, dict)])
    candidates = _dedupe_results(candidates)
    fetch_top_n = max(1, min(12, int(fetch_top_n or DEFAULT_RESEARCH_FETCH_TOP_N)))
    max_chars_per_source = max(500, min(10000, int(max_chars_per_source or 3000)))
    sources = []
    failures = []
    for candidate in candidates[:fetch_top_n]:
        url = str(candidate.get("url") or "").strip()
        if not url:
            continue
        source = {
            "title": str(candidate.get("title") or ""),
            "url": url,
            "query": str(candidate.get("query") or ""),
            "snippet": str(candidate.get("snippet") or "")[:500],
            "fetch_ok": False,
            "excerpt": "",
            "truncated": False,
            "content_type": "",
        }
        try:
            fetched = _fetch(url, max_chars=max_chars_per_source, timeout_sec=timeout_sec)
            excerpt = _redact_sensitive_text(str(fetched.get("text") or ""))
            source.update(
                {
                    "url": str(fetched.get("url") or url),
                    "content_type": str(fetched.get("content_type") or ""),
                    "excerpt": excerpt[:max_chars_per_source],
                    "truncated": bool(fetched.get("truncated")),
                    "fetch_ok": True,
                }
            )
        except Exception as exc:  # noqa: BLE001
            source["warning"] = f"{type(exc).__name__}: {exc}"
            failures.append({"url": url, "warning": source["warning"]})
        sources.append(source)
    fetched_sources = [item for item in sources if item.get("fetch_ok")]
    unresolved = []
    if not fetched_sources:
        unresolved.append("No pages were fetched successfully; try explicit source_urls or narrower queries.")
    if len(fetched_sources) < min(3, fetch_top_n):
        unresolved.append("Source coverage is thin; treat claims as provisional and run another brief with targeted queries.")
    return {
        "tool": "lcr_web_research_brief",
        "research_goal": research_goal,
        "query_plan": query_texts[:DEFAULT_BATCH_MAX_QUERIES],
        "search": {
            "query_count": search_payload.get("query_count"),
            "result_count": search_payload.get("result_count"),
            "warnings": search_payload.get("warnings") or [],
        },
        "sources": sources,
        "source_count": len(sources),
        "fetched_source_count": len(fetched_sources),
        "failures": failures[:10],
        "brief": _compose_extract_brief(research_goal, fetched_sources),
        "unresolved_questions": unresolved,
        "suggested_followup_queries": _suggest_followup_queries(research_goal, query_texts, fetched_sources),
        "citation_rule": "Use only URLs in sources for citations. Mark unfetched search snippets as unverified.",
    }


def _search(query: str, *, max_results: int, timeout_sec: int) -> dict[str, Any]:
    max_results = max(1, min(10, int(max_results or 5)))
    search_url = "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
    try:
        body, final_url, content_type = _download_text(search_url, timeout_sec=timeout_sec)
        parser = _DuckDuckGoParser()
        parser.feed(body)
        results = parser.results[:max_results]
        if not results:
            bing = _search_bing(query, max_results=max_results, timeout_sec=timeout_sec)
            bing["fallback_from"] = "duckduckgo_html"
            return bing
        return {
            "tool": "lcr_web_search",
            "query": query,
            "source": "duckduckgo_html",
            "url": final_url,
            "content_type": content_type,
            "results": results,
            "result_count": len(results),
            "warning": "" if results else "No parsed results; try a more specific query or fetch a known URL.",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "tool": "lcr_web_search",
            "query": query,
            "source": "duckduckgo_html",
            "results": [],
            "result_count": 0,
            "warning": f"Search failed: {type(exc).__name__}: {exc}",
        }


def _search_bing(query: str, *, max_results: int, timeout_sec: int) -> dict[str, Any]:
    search_url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query})
    try:
        body, final_url, content_type = _download_text(search_url, timeout_sec=timeout_sec)
        parser = _BingParser()
        parser.feed(body)
        results = parser.results[:max_results]
        return {
            "tool": "lcr_web_search",
            "query": query,
            "source": "bing_html",
            "url": final_url,
            "content_type": content_type,
            "results": results,
            "result_count": len(results),
            "warning": "" if results else "No parsed results from DuckDuckGo or Bing; try explicit source_urls or a more specific query.",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "tool": "lcr_web_search",
            "query": query,
            "source": "bing_html",
            "results": [],
            "result_count": 0,
            "warning": f"Search failed: {type(exc).__name__}: {exc}",
        }


def _normalize_query_specs(queries: Any) -> list[dict[str, Any]]:
    if not isinstance(queries, list) or not queries:
        raise ValueError("queries must be a non-empty array.")
    specs: list[dict[str, Any]] = []
    for item in queries[:DEFAULT_BATCH_MAX_QUERIES]:
        if isinstance(item, str):
            query = item.strip()
            max_results = 5
        elif isinstance(item, dict):
            query = str(item.get("query") or "").strip()
            max_results = int(item.get("max_results") or 5)
        else:
            continue
        if not query:
            continue
        specs.append({"query": query[:300], "max_results": max(1, min(10, max_results))})
    if not specs:
        raise ValueError("At least one non-empty query is required.")
    return specs


def _string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        raw = [value]
    elif isinstance(value, list):
        raw = value
    else:
        raw = []
    result = []
    for item in raw:
        text = str(item or "").strip()
        if not text:
            continue
        if _looks_secret_like(text):
            raise ValueError("Web research arguments cannot contain secret-like values.")
        result.append(text[:500])
    return result


def _dedupe_results(results: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    deduped = []
    for item in results:
        url = str(item.get("url") or "").strip()
        key = _canonical_url(url)
        if not url or key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _canonical_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    filtered = [(key, value) for key, value in query if not key.lower().startswith("utm_")]
    return urllib.parse.urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", urllib.parse.urlencode(filtered), ""))


def _derive_research_queries(goal: str) -> list[str]:
    compact = re.sub(r"\s+", " ", goal).strip()
    queries = [compact]
    lowered = compact.lower()
    if any(token in lowered for token in ["魔塔", "tower", "rpg", "game", "autotile", "sprite"]):
        queries.extend(
            [
                f"{compact} best practices",
                f"{compact} implementation guide",
                f"{compact} examples",
                "RPG autotile rules tilemap edge corner transition",
                "magic tower game design deterministic resource planning",
            ]
        )
    else:
        queries.extend([f"{compact} official documentation", f"{compact} guide", f"{compact} best practices"])
    return list(dict.fromkeys(query[:300] for query in queries if query))[:DEFAULT_BATCH_MAX_QUERIES]


def _compose_extract_brief(goal: str, sources: list[dict[str, Any]]) -> dict[str, Any]:
    bullets = []
    for index, source in enumerate(sources[:6], start=1):
        excerpt = re.sub(r"\s+", " ", str(source.get("excerpt") or source.get("snippet") or "")).strip()
        if not excerpt:
            continue
        bullets.append(
            {
                "source_index": index,
                "url": source.get("url"),
                "extract": excerpt[:500],
            }
        )
    return {
        "summary": (
            "Extractive source pack generated for the research goal. The model should synthesize conclusions "
            "from these excerpts and cite source URLs explicitly."
        ),
        "goal": goal,
        "source_extracts": bullets,
    }


def _suggest_followup_queries(goal: str, queries: list[str], sources: list[dict[str, Any]]) -> list[str]:
    suggestions = []
    if len(sources) < 3:
        suggestions.append(f"{goal} official documentation")
    suggestions.append(f"{goal} case study")
    suggestions.append(f"{goal} pitfalls")
    for query in queries:
        if "official" not in query.lower():
            suggestions.append(f"{query} official")
            break
    return list(dict.fromkeys(suggestions))[:5]


def _looks_secret_like(value: str) -> bool:
    if re.search(r"(?i)(authorization|bearer\s+|api[_-]?key|secret|cookie|token)", value):
        return True
    return bool(re.search(r"sk-[A-Za-z0-9_-]{8,}", value))


def _fetch(url: str, *, max_chars: int, timeout_sec: int) -> dict[str, Any]:
    _validate_public_url(url)
    body, final_url, content_type = _download_text(url, timeout_sec=timeout_sec)
    text = _html_to_text(body) if "html" in content_type.lower() or "<html" in body[:500].lower() else body
    text = _redact_sensitive_text(text)
    max_chars = max(500, min(20000, int(max_chars or DEFAULT_MAX_CHARS)))
    truncated = len(text) > max_chars
    return {
        "tool": "lcr_web_fetch",
        "url": final_url,
        "content_type": content_type,
        "text": text[:max_chars],
        "truncated": truncated,
        "char_count": len(text),
    }


def _download_text(url: str, *, timeout_sec: int) -> tuple[str, str, str]:
    _validate_public_url(url)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "LocalCodexRouter/0.1 (+https://local-codex-router.invalid)",
            "Accept": "text/html, text/plain, application/json;q=0.8, */*;q=0.5",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=max(5, min(60, int(timeout_sec or DEFAULT_TIMEOUT_SEC)))) as response:  # noqa: S310
        content_type = str(response.headers.get("Content-Type") or "text/plain")
        charset = response.headers.get_content_charset() or "utf-8"
        raw = response.read(1_000_000)
        text = raw.decode(charset, errors="replace")
        return text, str(response.geturl() or url), content_type


def _validate_public_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Only public HTTP(S) URLs are supported.")
    host = parsed.hostname or ""
    if not host:
        raise ValueError("URL host is required.")
    if host.lower() in {"localhost"} or host.endswith(".local"):
        raise ValueError("Localhost and .local URLs are blocked for web research tools.")
    try:
        addresses = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"Cannot resolve host: {host}") from exc
    for entry in addresses:
        ip_text = entry[4][0]
        try:
            ip = ipaddress.ip_address(ip_text)
        except ValueError:
            continue
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            raise ValueError("Private, loopback, link-local, multicast, and reserved addresses are blocked.")


class _DuckDuckGoParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict[str, str]] = []
        self._active: dict[str, str] | None = None
        self._capture_title = False
        self._capture_snippet = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        classes = attr.get("class", "")
        if tag == "a" and "result__a" in classes:
            self._active = {"title": "", "url": _clean_ddg_url(attr.get("href", "")), "snippet": ""}
            self._capture_title = True
        elif self._active is not None and tag in {"a", "div"} and ("result__snippet" in classes or "result__body" in classes):
            self._capture_snippet = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._capture_title:
            self._capture_title = False
            if self._active is not None and self._active.get("url"):
                self.results.append({key: value.strip() for key, value in self._active.items()})
                self._active = None
        if tag in {"a", "div"}:
            self._capture_snippet = False

    def handle_data(self, data: str) -> None:
        if self._active is None:
            return
        text = html.unescape(data).strip()
        if not text:
            return
        if self._capture_title:
            self._active["title"] = (self._active.get("title", "") + " " + text).strip()
        elif self._capture_snippet:
            self._active["snippet"] = (self._active.get("snippet", "") + " " + text).strip()


def _clean_ddg_url(url: str) -> str:
    text = html.unescape(url or "")
    parsed = urllib.parse.urlparse(text)
    query = urllib.parse.parse_qs(parsed.query)
    if "uddg" in query and query["uddg"]:
        return str(query["uddg"][0])
    return text


class _BingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict[str, str]] = []
        self._active: dict[str, str] | None = None
        self._depth = 0
        self._capture_title = False
        self._capture_snippet = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        classes = attr.get("class", "")
        if self._active is None and tag == "li" and "b_algo" in classes:
            self._active = {"title": "", "url": "", "snippet": ""}
            self._depth = 1
            return
        if self._active is None:
            return
        self._depth += 1
        if tag == "a" and not self._active.get("url"):
            href = attr.get("href", "")
            if href.startswith(("http://", "https://")):
                self._active["url"] = _clean_bing_url(href)
                self._capture_title = True
        elif tag == "p":
            self._capture_snippet = True

    def handle_endtag(self, tag: str) -> None:
        if self._active is None:
            return
        if tag == "a":
            self._capture_title = False
        elif tag == "p":
            self._capture_snippet = False
        self._depth -= 1
        if self._depth <= 0:
            if self._active.get("url") and self._active.get("title"):
                self.results.append({key: value.strip() for key, value in self._active.items()})
            self._active = None
            self._capture_title = False
            self._capture_snippet = False

    def handle_data(self, data: str) -> None:
        if self._active is None:
            return
        text = html.unescape(data).strip()
        if not text:
            return
        if self._capture_title:
            self._active["title"] = (self._active.get("title", "") + " " + text).strip()
        elif self._capture_snippet:
            self._active["snippet"] = (self._active.get("snippet", "") + " " + text).strip()


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
        elif tag in {"p", "br", "li", "h1", "h2", "h3", "h4", "tr"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in {"p", "li", "h1", "h2", "h3", "h4", "tr"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = html.unescape(data).strip()
        if text:
            self.parts.append(text)


def _html_to_text(markup: str) -> str:
    parser = _TextExtractor()
    parser.feed(markup)
    text = " ".join(parser.parts)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _clean_bing_url(url: str) -> str:
    text = html.unescape(url or "")
    parsed = urllib.parse.urlparse(text)
    if "bing.com" not in parsed.netloc.lower():
        return text
    query = urllib.parse.parse_qs(parsed.query)
    raw = (query.get("u") or [""])[0]
    if not raw:
        return text
    if raw.startswith(("http://", "https://")):
        return raw
    candidate = raw[2:] if raw.startswith("a1") else raw
    try:
        padding = "=" * (-len(candidate) % 4)
        decoded = base64.urlsafe_b64decode((candidate + padding).encode("ascii")).decode("utf-8", errors="replace")
        if decoded.startswith(("http://", "https://")):
            return decoded
    except Exception:
        return text
    return text


def _redact_sensitive_text(text: str) -> str:
    patterns = [
        (re.compile(r"(?i)authorization\s*:\s*bearer\s+[A-Za-z0-9._~+/=-]+"), "Authorization: [REDACTED]"),
        (re.compile(r"(?i)(api[_-]?key|token|secret|cookie)\s*[:=]\s*[A-Za-z0-9._~+/=-]{8,}"), r"\1=[REDACTED]"),
        (re.compile(r"sk-[A-Za-z0-9_-]{16,}"), "sk-[REDACTED]"),
    ]
    redacted = text
    for pattern, replacement in patterns:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def _tool_text(payload: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}]}


def _result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _read_message(stream: BinaryIO) -> dict[str, Any] | None:
    global _OUTPUT_FRAMING
    first = _read_first_nonempty_byte(stream)
    if not first:
        return None
    if first == b"{":
        _OUTPUT_FRAMING = "raw"
        return json.loads(_read_json_object(stream, first).decode("utf-8"))
    _OUTPUT_FRAMING = "header"
    headers: dict[str, str] = {}
    line = first + stream.readline()
    while line and line.strip():
        text = line.decode("ascii", errors="replace")
        if ":" in text:
            key, value = text.split(":", 1)
            headers[key.lower()] = value.strip()
        line = stream.readline()
    length = int(headers.get("content-length") or 0)
    if length <= 0:
        return None
    return json.loads(stream.read(length).decode("utf-8"))


def _read_first_nonempty_byte(stream: BinaryIO) -> bytes:
    while True:
        chunk = stream.read(1)
        if not chunk:
            return b""
        if chunk in b" \t\r\n":
            continue
        return chunk


def _read_json_object(stream: BinaryIO, first: bytes) -> bytes:
    buffer = bytearray(first)
    depth = 1
    in_string = False
    escaped = False
    while depth > 0:
        chunk = stream.read(1)
        if not chunk:
            break
        char = chunk[0]
        buffer.extend(chunk)
        if in_string:
            if escaped:
                escaped = False
            elif char == 92:
                escaped = True
            elif char == 34:
                in_string = False
            continue
        if char == 34:
            in_string = True
        elif char == 123:
            depth += 1
        elif char == 125:
            depth -= 1
    return bytes(buffer)


def _write_message(stream: BinaryIO, message: dict[str, Any]) -> None:
    body = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if _OUTPUT_FRAMING == "raw":
        stream.write(body + b"\n")
        stream.flush()
        return
    stream.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    stream.write(body)
    stream.flush()


def _debug(event: str, **fields: Any) -> None:
    try:
        raw_path = os.environ.get("LCR_MCP_DEBUG_LOG")
        if not raw_path:
            local_app_data = os.environ.get("LOCALAPPDATA")
            if not local_app_data:
                return
            raw_path = str(Path(local_app_data) / "LCR" / "mcp" / "lcr_web_debug.jsonl")
        path = Path(raw_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {"timestamp": datetime.now(timezone.utc).isoformat(), "event": event, **fields}
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    main()
