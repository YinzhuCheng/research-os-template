param(
  [string[]]$HtmlDocs = @("docs\start-here.html", "docs\domain-modes.html", "docs\technical-report.html", "docs\codex-browser-copilot.html", "PUBLIC\index.html", "PUBLIC\copilot.html")
)

$ErrorActionPreference = "Stop"

foreach ($path in $HtmlDocs) {
  if (!(Test-Path -LiteralPath $path)) {
    throw "HTML document missing: $path"
  }
  $html = Get-Content -Raw -Encoding UTF8 -LiteralPath $path
  $required = @("<!doctype html>", "<html", "<meta name=""viewport""", "</html>")
  foreach ($item in $required) {
    if ($html.ToLowerInvariant() -notlike "*$($item.ToLowerInvariant())*") {
      throw "HTML check failed for ${path}: missing $item"
    }
  }
  $lastClose = $html.LastIndexOf("</html>", [System.StringComparison]::OrdinalIgnoreCase)
  if ($lastClose -lt 0) {
    throw "HTML check failed for ${path}: missing closing html tag."
  }
  $tail = $html.Substring($lastClose + 7)
  if ($tail.Trim().Length -gt 0) {
    $preview = $tail.Trim()
    if ($preview.Length -gt 160) { $preview = $preview.Substring(0, 160) }
    throw "HTML check failed for ${path}: non-whitespace content after </html>: $preview"
  }
  if ($html -match "(?i)<script\s+[^>]*src\s*=") {
    throw "HTML check failed for ${path}: external script src is not allowed."
  }
  if ($html -match "(?i)<link\s+[^>]*href\s*=\s*['""]https?://") {
    throw "HTML check failed for ${path}: remote stylesheet/font link is not allowed."
  }
  if ($path -like "docs\*.html") {
    foreach ($needle in @("README.md", "work_order.yaml", "phase_gate.yaml", "PUBLIC/index.html")) {
      if ($html -notlike "*$needle*") {
        throw "HTML check failed for ${path}: missing repository link $needle"
      }
    }
    if ($html -notlike "*<svg*") {
      throw "HTML check failed for ${path}: expected an inline SVG diagram."
    }
  }
  Write-Output "HTML doc OK: $path"
}

Write-Output "HTML documentation check passed."
