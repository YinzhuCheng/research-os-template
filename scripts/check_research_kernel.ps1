param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Require-File([string]$Path) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Required research kernel file missing: $Path" }
}

function Require-Text([string]$Path, [string]$Pattern) {
  $full = Join-Path $Root $Path
  Require-File $Path
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $full
  if ($text -notmatch $Pattern) { throw "Research kernel check failed: $Path missing $Pattern" }
}

$coreObjects = @(
  "candidate",
  "evaluator_contract",
  "evaluation_result",
  "belief_state",
  "search_trace",
  "negative_result",
  "next_action_policy",
  "human_judgment_gate"
)

$computationFields = @(
  "metric_or_check",
  "formula_or_procedure",
  "inputs",
  "units_or_scale",
  "acceptance_threshold",
  "resource_estimate",
  "failure_mode",
  "replay_note"
)

Require-File "config\schemas\research_kernel.schema.json"
Require-File "templates\yaml\research_kernel.template.yaml"
Require-File "templates\research_kernel\research_cycle.template.yaml"
Require-File "skills\research-os-research-kernel\SKILL.md"
Require-File "skills\research-os-research-kernel\references\kernel_workflow.md"

Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "config\schemas\research_kernel.schema.json") | ConvertFrom-Json | Out-Null

foreach ($objectName in $coreObjects) {
  Require-Text "config\schemas\research_kernel.schema.json" $objectName
  Require-Text "templates\yaml\research_kernel.template.yaml" $objectName
  Require-Text "templates\research_kernel\research_cycle.template.yaml" $objectName
  Require-Text "skills\research-os-research-kernel\SKILL.md" $objectName
}

foreach ($field in $computationFields) {
  Require-Text "config\schemas\research_kernel.schema.json" $field
  Require-Text "templates\yaml\research_kernel.template.yaml" $field
  Require-Text "templates\research_kernel\research_cycle.template.yaml" $field
  Require-Text "skills\research-os-research-kernel\references\kernel_workflow.md" $field
}

Require-Text "skills\research-os-orchestrator\SKILL.md" "research-os-research-kernel"
Require-Text "skills\research-os-orchestrator\references\routing.md" "generate -> evaluate -> update -> human_gate"
Require-Text "docs\doc_map.yaml" "research_kernel"

Write-Output "Research kernel validation passed."
