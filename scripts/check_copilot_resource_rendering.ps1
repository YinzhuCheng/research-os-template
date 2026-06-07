param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Require-Text([string]$Path, [string]$Pattern) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Missing file: $Path" }
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $full
  if ($text -notmatch $Pattern) { throw "Rendering check failed: $Path missing $Pattern" }
}

Require-Text "PUBLIC\copilot.html" "Research OS Copilot"
Require-Text "PUBLIC\copilot.html" "settingsPanel"
Require-Text "PUBLIC\copilot.html" "researchOS.uiPreferences.v1"
Require-Text "PUBLIC\copilot.html" "Developer Dark"
Require-Text "PUBLIC\copilot.html" "Editorial Report"
Require-Text "PUBLIC\copilot.html" "final papers default to English"
Require-Text "PUBLIC\copilot.html" "api/intake"
Require-Text "PUBLIC\copilot.html" "Other"
Require-Text "PUBLIC\copilot.html" "download_reference_links.ps1"
Require-Text "PUBLIC\copilot.html" "Overview"
Require-Text "PUBLIC\copilot.html" "Literature"
Require-Text "PUBLIC\copilot.html" "Theory"
Require-Text "PUBLIC\copilot.html" "Experiment"
Require-Text "PUBLIC\copilot.html" "Evidence Board"
Require-Text "PUBLIC\copilot.html" "Repository Links"
Require-Text "PUBLIC\copilot.html" "copilot_state.json"
Require-Text "PUBLIC\copilot.html" "evidence_board.json"

Require-Text "docs\codex-browser-copilot.html" "material_input"
Require-Text "docs\codex-browser-copilot.html" "pending_intake_analysis"
Require-Text "docs\codex-browser-copilot.html" "three targeted questions"
Require-Text "docs\codex-browser-copilot.html" "PUBLIC/copilot.html"
Require-Text "docs\doc_map.yaml" "copilot"
Require-Text "PUBLIC\dashboard_data.json" "copilot.html"

Write-Output "Copilot resource rendering validation passed."
