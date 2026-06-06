param(
  [string]$Dashboard = "PUBLIC\index.html"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $Dashboard)) {
  throw "Dashboard missing: $Dashboard"
}

$html = Get-Content -Raw -Encoding UTF8 -LiteralPath $Dashboard
$required = @(
  "<!doctype html>",
  "dashboard_data.json",
  "renderMarkdown",
  "Codex Research OS",
  "PUBLIC/index.html",
  "feasibility",
  "resource",
  "live evidence"
)

foreach ($item in $required) {
  if ($html -notlike "*$item*") {
    throw "Dashboard check failed: missing $item"
  }
}

Get-Content -Raw -Encoding UTF8 -LiteralPath "PUBLIC\dashboard_data.json" | ConvertFrom-Json | Out-Null
Write-Output "Dashboard static check passed."
