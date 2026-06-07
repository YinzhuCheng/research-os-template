param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Read-Text([string]$Path) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Missing required file: $Path" }
  Get-Content -Raw -Encoding UTF8 -LiteralPath $full
}

function Require-Text([string]$Path, [string]$Needle) {
  $text = Read-Text $Path
  if ($text -notlike "*$Needle*") { throw "Missing '$Needle' in $Path" }
}

$flow = Read-Text "config\research_flow.yaml"
$flowSchema = Read-Text "config\schemas\research_flow.schema.json"
$skillsReadme = Read-Text "skills\README.md"
$routing = Read-Text "skills\research-os-orchestrator\references\routing.md"
$agents = Read-Text "AGENTS.md"
$docMap = Read-Text "docs\doc_map.yaml"
$architecture = Read-Text "docs\architecture.md"
$dashboard = Read-Text "PUBLIC\dashboard_data.json"
$processContract = Read-Text "docs\process-contract.md"

$sequence = @(
  "initialization_intake",
  "loop_acceptance_gate",
  "loop_plan_alignment",
  "loop_user_decision",
  "loop_execute_analyze",
  "final_product_selection",
  "final_product_production",
  "export_release_gate"
)

foreach ($stage in $sequence) {
  foreach ($path in @("config\research_flow.yaml")) {
    Require-Text $path $stage
  }
}

Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "config\schemas\research_flow.schema.json") | ConvertFrom-Json | Out-Null

$requiredSkillMatches = [regex]::Matches($flow, "(?m)^\s*required_skill:\s*(research-os-[a-z0-9-]+)") |
  ForEach-Object { $_.Groups[1].Value } |
  Sort-Object -Unique

if ($requiredSkillMatches.Count -lt 5) {
  throw "Expected several required skills in config/research_flow.yaml."
}

$workOrder = Read-Text "CONTROL\work_order.yaml"
foreach ($skillName in $requiredSkillMatches) {
  $skillPath = Join-Path $Root "skills\$skillName\SKILL.md"
  if (!(Test-Path -LiteralPath $skillPath)) {
    $plannedNeedle = "skills/$skillName/"
    if ($workOrder -notlike "*$plannedNeedle*") {
      throw "Flow references missing skill: $skillName"
    }
    Write-Output "Flow references planned skill from current work order: $skillName"
    continue
  }
  if ($skillsReadme -notmatch [regex]::Escape($skillName)) { throw "skills/README.md missing flow skill: $skillName" }
}

$mustMention = @(
  "config/research_flow.yaml",
  "user_macro_phases",
  "choice_prompt_contract",
  "initialization_intake",
  "loop_acceptance_gate",
  "final_product_selection",
  "final_product_production",
  "export_release_gate",
  "research-os-orchestrator",
  "research-os-research-kernel",
  "research-os-final-product",
  "exactly three targeted questions",
  "loop_acceptance_gate",
  "free-form"
)

foreach ($needle in $mustMention) {
  if ($flow -notlike "*$needle*" -and $flowSchema -notlike "*$needle*" -and $routing -notlike "*$needle*" -and $skillsReadme -notlike "*$needle*" -and $agents -notlike "*$needle*" -and $docMap -notlike "*$needle*" -and $architecture -notlike "*$needle*" -and $dashboard -notlike "*$needle*" -and $processContract -notlike "*$needle*") {
    throw "Process governance missing required concept: $needle"
  }
}

Require-Text "docs\doc_map.yaml" "process_contract"
Require-Text "docs\doc_map.yaml" "config/research_flow.yaml"
Require-Text "PUBLIC\dashboard_data.json" "../docs/process-contract.md"
Require-Text "PUBLIC\dashboard_data.json" "../config/research_flow.yaml"
Require-Text "docs\architecture.md" "config/research_flow.yaml"
Require-Text "docs\architecture.md" "Final Product Tracks"
Require-Text "docs\architecture.md" "Git-backed archives"
Require-Text "AGENTS.md" "Use Repo Skills First"
Require-Text "AGENTS.md" "Canonical Flow"
Require-Text "docs\process-contract.md" "Choice Prompt Contract"
Require-Text "docs\process-contract.md" "Archive Contract"

Write-Output "Research flow governance check passed."
