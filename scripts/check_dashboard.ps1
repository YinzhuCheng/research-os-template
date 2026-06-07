param(
  [string]$DashboardData = "PUBLIC\dashboard_data.json"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $DashboardData)) {
  throw "Dashboard data missing: $DashboardData"
}

$data = Get-Content -Raw -Encoding UTF8 -LiteralPath $DashboardData | ConvertFrom-Json
if ($data.project.title -ne "Research OS Desktop") { throw "Dashboard data has the wrong product title." }
if ($data.project.primary_entrypoint -notlike "*Tauri*React*Python sidecar*") { throw "Dashboard data must be desktop-app first." }

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

Write-Output "Dashboard data check passed."
