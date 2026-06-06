param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Require-File([string]$Path) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Missing copilot file: $Path" }
}

function Require-Text([string]$Path, [string]$Pattern) {
  $full = Join-Path $Root $Path
  Require-File $Path
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $full
  if ($text -notmatch $Pattern) { throw "Copilot schema check failed: $Path missing $Pattern" }
}

$schemaFiles = @(
  "config\schemas\copilot_intake.schema.json",
  "config\schemas\copilot_questions.schema.json",
  "config\schemas\copilot_initialization_report.schema.json"
)

foreach ($schema in $schemaFiles) {
  Require-File $schema
  Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root $schema) | ConvertFrom-Json | Out-Null
  Write-Output "Copilot JSON schema OK: $schema"
}

Require-File "templates\yaml\copilot_intake.template.yaml"
Require-File "templates\yaml\copilot_questions.template.yaml"
Require-File "templates\yaml\copilot_initialization_report.template.yaml"

foreach ($field in @("session_id", "free_text", "uploaded_files", "source_links", "privacy_default", "material_hashes", "status")) {
  Require-Text "config\schemas\copilot_intake.schema.json" $field
  Require-Text "templates\yaml\copilot_intake.template.yaml" $field
}

foreach ($field in @("question_id", "reason_for_asking", "recommended_answer", "options", "free_text_other", "plan_impact")) {
  Require-Text "config\schemas\copilot_questions.schema.json" $field
  Require-Text "templates\yaml\copilot_questions.template.yaml" $field
}

foreach ($field in @("research_type", "motivation", "expected_goals", "contribution_claims", "related_work_map", "reference_links", "download_script", "theory_track", "experiment_track", "minimum_validation", "repository_resource_links")) {
  Require-Text "config\schemas\copilot_initialization_report.schema.json" $field
  Require-Text "templates\yaml\copilot_initialization_report.template.yaml" $field
}

$questionsTemplate = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "templates\yaml\copilot_questions.template.yaml")
$questionCount = ([regex]::Matches($questionsTemplate, "question_id:\s+Q-[0-9]{2}")).Count
if ($questionCount -ne 3) {
  throw "Copilot question template must contain exactly three targeted questions; found $questionCount."
}

Write-Output "Copilot intake/question/initialization schema validation passed."
