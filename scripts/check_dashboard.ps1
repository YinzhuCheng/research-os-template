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
  "Research OS Desktop",
  "dashboard_data.json",
  "docs/desktop-app.md",
  "research_state.json",
  "Tauri",
  "Python sidecar",
  ".rosproj"
)

foreach ($item in $required) {
  if ($html -notlike "*$item*") {
    throw "Dashboard check failed: missing $item"
  }
}

$data = Get-Content -Raw -Encoding UTF8 -LiteralPath "PUBLIC\dashboard_data.json" | ConvertFrom-Json
foreach ($label in @("Desktop App", "Project Sandbox", "Approvals", "Final Products", "Archives", "Risk Register")) {
  if (!($data.status.label -contains $label)) {
    throw "Dashboard data missing status: $label"
  }
}

$requiredDocumentPaths = @(
  "../docs/desktop-app.md",
  "../docs/architecture.md",
  "../docs/security-risk.md",
  "../docs/testing.md",
  "../docs/migration.md",
  "research_state.json",
  "archive_index.json",
  "../config/schemas/research_state.schema.json",
  "../config/schemas/intake_packet.schema.json",
  "../scripts/check_desktop_app.ps1"
)

foreach ($path in $requiredDocumentPaths) {
  if (!($data.documents.path -contains $path)) {
    throw "Dashboard data missing document path: $path"
  }
}

Write-Output "Dashboard static check passed."
