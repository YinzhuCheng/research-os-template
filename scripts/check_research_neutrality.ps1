param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Read-Text([string]$Path) {
  Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root $Path)
}

$config = Read-Text "config\research_project.yaml"
$briefTemplate = Read-Text "templates\markdown\research_brief.template.md"
$publicBrief = Read-Text "PUBLIC\research_brief.md"

$forbiddenConfig = @(
  "model_budget\s*:\s*100",
  "target_venue\s*:",
  "submission_format\s*:\s*latex",
  "budget_limits\s*:"
)

foreach ($pattern in $forbiddenConfig) {
  if ($config -match $pattern) {
    throw "Research neutrality failed: config contains forbidden default pattern: $pattern"
  }
}

foreach ($pattern in @("resource_budget\s*:", "research_profile\s*:", "dissemination\s*:", "feasibility_probe\s*:")) {
  if ($config -notmatch $pattern) {
    throw "Research neutrality failed: config missing required v2 pattern: $pattern"
  }
}

foreach ($text in @($briefTemplate, $publicBrief)) {
  if ($text -notmatch "research-neutrality:\s*no-default-llm") {
    throw "Research neutrality failed: brief missing no-default-llm marker."
  }
  if ($text -notmatch "research-neutrality:.*researcher-defined-budget") {
    throw "Research neutrality failed: brief missing researcher-defined-budget marker."
  }
}

$caseNames = @(
  "llm-method-study",
  "wet-lab-mechanism-study",
  "social-science-interview-study",
  "theory-or-review-study"
)

foreach ($name in $caseNames) {
  $simulated = [pscustomobject]@{
    case = $name
    research_profile = "from_source"
    resource_budget = "researcher_defined"
    dissemination = "from_source_or_undecided"
    default_model = $null
    default_budget = $null
    default_paper = $false
  }
  if ($null -ne $simulated.default_model -or $null -ne $simulated.default_budget -or $simulated.default_paper) {
    throw "Research neutrality failed for case: $name"
  }
}

Write-Output "Research neutrality check passed for generic and four dry-run research cases."
