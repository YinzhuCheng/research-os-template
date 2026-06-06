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
$technical = Read-Text "docs\technical-report.html"
$dashboard = Read-Text "PUBLIC\dashboard_data.json"

$sequence = @(
  "material_intake",
  "targeted_questions",
  "initialization",
  "research_kernel",
  "domain_or_general_route",
  "feasibility_or_evidence",
  "execution_harness",
  "analysis",
  "acceptance_gate",
  "next_loop_or_export"
)

foreach ($stage in $sequence) {
  foreach ($path in @("config\research_flow.yaml", "docs\process-contract.md", "skills\research-os-orchestrator\references\routing.md")) {
    Require-Text $path $stage
  }
}

Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "config\schemas\research_flow.schema.json") | ConvertFrom-Json | Out-Null

$requiredSkillMatches = [regex]::Matches($flow, "(?m)^\s*required_skill:\s*(research-os-[a-z0-9-]+)") |
  ForEach-Object { $_.Groups[1].Value } |
  Sort-Object -Unique

if ($requiredSkillMatches.Count -lt 7) {
  throw "Expected several required skills in config/research_flow.yaml."
}

foreach ($skillName in $requiredSkillMatches) {
  $skillPath = Join-Path $Root "skills\$skillName\SKILL.md"
  if (!(Test-Path -LiteralPath $skillPath)) { throw "Flow references missing skill: $skillName" }
  if ($skillsReadme -notmatch [regex]::Escape($skillName)) { throw "skills/README.md missing flow skill: $skillName" }
}

$mustMention = @(
  "config/research_flow.yaml",
  "docs/process-contract.md",
  "skills/README.md",
  "research-os-orchestrator",
  "research-os-research-kernel",
  "exactly three targeted questions",
  "Anti-Spaghetti Skill Rule"
)

foreach ($needle in $mustMention) {
  if ($routing -notlike "*$needle*" -and $skillsReadme -notlike "*$needle*" -and $agents -notlike "*$needle*" -and $docMap -notlike "*$needle*" -and $technical -notlike "*$needle*" -and $dashboard -notlike "*$needle*") {
    throw "Process governance missing required concept: $needle"
  }
}

Require-Text "docs\doc_map.yaml" "process_contract"
Require-Text "docs\doc_map.yaml" "config/research_flow.yaml"
Require-Text "PUBLIC\dashboard_data.json" "../docs/process-contract.md"
Require-Text "PUBLIC\dashboard_data.json" "../config/research_flow.yaml"
Require-Text "docs\technical-report.html" "config/research_flow.yaml"
Require-Text "AGENTS.md" "Use Repo Skills First"
Require-Text "AGENTS.md" "Canonical Flow"

Write-Output "Research flow governance check passed."
