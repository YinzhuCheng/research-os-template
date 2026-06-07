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
  "renderJsonDocument",
  "renderYamlDocument",
  "settingsPanel",
  "researchOS.uiPreferences.v1",
  "data-theme",
  "Developer Dark",
  "Editorial Report",
  "Natural-Language UI Goal",
  "final papers default to English",
  "phasebar",
  "action-groups",
  "finalProductPanel",
  "archivePanel",
  "/api/archive-snapshot",
  "archive_index.json",
  "Codex Research OS",
  "PUBLIC/index.html",
  "copilot.html",
  "material-first",
  "process contract",
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
if (!($data.status.label -contains "P0/P1 Hardening")) {
  throw "Dashboard data missing P0/P1 Hardening status."
}
if (!($data.status.label -contains "Copilot Usability")) {
  throw "Dashboard data missing Copilot Usability status."
}
if (!($data.status.label -contains "UI Settings")) {
  throw "Dashboard data missing UI Settings status."
}
if (!($data.status.label -contains "Macro Phases")) {
  throw "Dashboard data missing Macro Phases status."
}
if (!($data.status.label -contains "Final Products")) {
  throw "Dashboard data missing Final Products status."
}
if (!($data.status.label -contains "Archives")) {
  throw "Dashboard data missing Archives status."
}
$requiredDocumentPaths = @(
  "archive_index.json",
  "../docs/environment.md",
  "../docs/process-contract.md",
  "../config/research_flow.yaml",
  "../config/schemas/choice_prompt.schema.json",
  "../config/schemas/final_product_plan.schema.json",
  "../config/schemas/archive_record.schema.json",
  "../templates/yaml/final_product_plan.template.yaml",
  "evidence_board.json",
  "run_monitor.json",
  "../config/schemas/copilot_answers.schema.json",
  "../config/schemas/copilot_confirmation.schema.json",
  "../config/schemas/experiment_run.schema.json",
  "../config/schemas/adapter_contract.schema.json",
  "../evals/README.md",
  "../scripts/install_environment.ps1",
  "../scripts/check_environment.ps1"
)

foreach ($path in $requiredDocumentPaths) {
  if (!($data.documents.path -contains $path)) {
    throw "Dashboard data missing document path: $path"
  }
}

Write-Output "Dashboard static check passed."
