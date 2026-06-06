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
  "copilot.html",
  "material-first",
  "environment",
  "feasibility",
  "resource",
  "live evidence"
)

foreach ($item in $required) {
  if ($html -notlike "*$item*") {
    throw "Dashboard check failed: missing $item"
  }
}

$data = Get-Content -Raw -Encoding UTF8 -LiteralPath "PUBLIC\dashboard_data.json" | ConvertFrom-Json
$requiredDocumentPaths = @(
  "../docs/environment.md",
  "../scripts/install_environment.ps1",
  "../scripts/check_environment.ps1"
)

foreach ($path in $requiredDocumentPaths) {
  if (!($data.documents.path -contains $path)) {
    throw "Dashboard data missing document path: $path"
  }
}

Write-Output "Dashboard static check passed."
