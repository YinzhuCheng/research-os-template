param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Require-Text([string]$Path, [string]$Pattern) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Missing router file: $Path" }
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $full
  if ($text -notmatch $Pattern) { throw "Router check failed: $Path missing $Pattern" }
}

$skills = @(
  "research-os-math-discovery",
  "research-os-applied-math-modeling",
  "research-os-ml-research-protocol",
  "research-os-cs-research-artifact",
  "research-os-statistical-inference"
)

Require-Text "skills\research-os-orchestrator\SKILL.md" "domain profile"
Require-Text "skills\research-os-orchestrator\SKILL.md" "research-os-research-kernel"
Require-Text "skills\research-os-orchestrator\references\routing.md" "domain_profiles"
Require-Text "skills\research-os-orchestrator\references\routing.md" "Anti-Spaghetti Skill Rule"
Require-Text "skills\research-os-research-kernel\SKILL.md" "evaluator_contract"

foreach ($skill in $skills) {
  Require-Text "skills\research-os-orchestrator\references\routing.md" $skill
  Require-Text "skills\$skill\SKILL.md" "research-os-execution-harness"
  Require-Text "skills\$skill\SKILL.md" "research-os-research-kernel"
  Require-Text "skills\$skill\SKILL.md" "domain_profiles"
}

Require-Text "docs\architecture.md" "domain_profiles"
Require-Text "docs\architecture.md" "research-os-math-discovery"

Write-Output "Domain router validation passed."
