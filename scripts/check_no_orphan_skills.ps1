param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Read-Text([string]$Path) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Missing governance file: $Path" }
  Get-Content -Raw -Encoding UTF8 -LiteralPath $full
}

$skillsDir = Join-Path $Root "skills"
if (!(Test-Path -LiteralPath $skillsDir)) { throw "Skills directory missing." }

$skillsReadme = Read-Text "skills\README.md"
$routing = Read-Text "skills\research-os-orchestrator\references\routing.md"
$researchFlow = Read-Text "config\research_flow.yaml"
$docMap = Read-Text "docs\doc_map.yaml"
$technicalReport = Read-Text "docs\technical-report.html"

$skills = Get-ChildItem -LiteralPath $skillsDir -Directory | Where-Object {
  Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

foreach ($skill in $skills) {
  if ($skillsReadme -notmatch [regex]::Escape($skill.Name)) {
    throw "Skill $($skill.Name) is missing from skills/README.md."
  }
}

$routedSkillMatches = [regex]::Matches($routing, "research-os-[a-z0-9-]+") | ForEach-Object { $_.Value } | Sort-Object -Unique
foreach ($skillName in $routedSkillMatches) {
  $skillPath = Join-Path $skillsDir "$skillName\SKILL.md"
  if (!(Test-Path -LiteralPath $skillPath)) {
    throw "Routing references missing skill: $skillName"
  }
}

if ($routing -notmatch [regex]::Escape("research-os-research-kernel")) {
  throw "Main routing missing required skill: research-os-research-kernel"
}

foreach ($required in @("research-os-research-kernel", "research-os-orchestrator")) {
  if ($skillsReadme -notmatch [regex]::Escape($required)) { throw "skills/README.md missing required skill: $required" }
  if ($technicalReport -notmatch [regex]::Escape($required)) { throw "Technical report missing required skill: $required" }
}

foreach ($docNeedle in @("research_kernel", "research_kernel_schema", "research_kernel_template")) {
  if ($docMap -notmatch $docNeedle) { throw "docs/doc_map.yaml missing $docNeedle" }
}

if ($routing -notmatch "Anti-Spaghetti Skill Rule") {
  throw "Routing must state the anti-spaghetti skill rule."
}

if ($researchFlow -notmatch "canonical_sequence") {
  throw "Research flow must state canonical_sequence."
}

foreach ($required in @("research-os-orchestrator", "research-os-copilot", "research-os-research-kernel", "research-os-execution-harness")) {
  if ($researchFlow -notmatch [regex]::Escape($required)) { throw "config/research_flow.yaml missing required skill: $required" }
  if ($skillsReadme -notmatch [regex]::Escape($required)) { throw "skills/README.md missing trigger matrix skill: $required" }
}

Write-Output "No orphan skill validation passed for $($skills.Count) skill(s)."
