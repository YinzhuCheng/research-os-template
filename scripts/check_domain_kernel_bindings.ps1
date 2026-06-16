param(
  [string]$ProfilesRoot = "domain_profiles",
  [string]$TemplateRoot = "templates\domain"
)

$ErrorActionPreference = "Stop"

$expectedDomains = @{
  "fundamental-mathematics" = "conjecture_card"
  "applied-mathematics" = "model_candidate"
  "machine-learning" = "task_card"
  "computer-science" = "problem_spec"
  "statistics" = "estimand_card"
}

$coreObjects = @(
  "candidate:",
  "evaluator_contract:",
  "evaluation_result:",
  "belief_state:",
  "search_trace:",
  "negative_result:",
  "next_action_policy:",
  "human_judgment_gate:"
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

$templateFiles = @{
  "fundamental-mathematics" = "math_discovery_case.template.yaml"
  "applied-mathematics" = "applied_math_model_case.template.yaml"
  "machine-learning" = "ml_research_case.template.yaml"
  "computer-science" = "cs_research_case.template.yaml"
  "statistics" = "statistical_inference_case.template.yaml"
}

foreach ($domain in $expectedDomains.Keys) {
  $profile = Join-Path $ProfilesRoot "$domain\profile.yaml"
  if (!(Test-Path -LiteralPath $profile)) { throw "Missing domain profile: $profile" }
  $profileText = Get-Content -Raw -Encoding UTF8 -LiteralPath $profile
  if ($profileText -notmatch "kernel_bindings:") { throw "Domain $domain missing kernel_bindings." }
  if ($profileText -notmatch [regex]::Escape($expectedDomains[$domain])) {
    throw "Domain $domain missing expected candidate binding $($expectedDomains[$domain])."
  }
  foreach ($objectName in $coreObjects) {
    if ($profileText -notlike "*$objectName*") { throw "Domain $domain missing kernel object $objectName" }
  }
  foreach ($field in $computationFields) {
    if ($profileText -notlike "*$field*") { throw "Domain $domain missing computation field $field" }
  }
  if ($profileText -notmatch "computation_checklist_required:\s+true") {
    throw "Domain $domain must require computation checklist."
  }

  $template = Join-Path $TemplateRoot "$domain\$($templateFiles[$domain])"
  if (!(Test-Path -LiteralPath $template)) { throw "Missing domain template: $template" }
  $templateText = Get-Content -Raw -Encoding UTF8 -LiteralPath $template
  foreach ($field in @("research_kernel:", "evaluator_contracts:", "search_trace_required:", "negative_result_policy:", "human_judgment_gate:")) {
    if ($templateText -notlike "*$field*") { throw "Domain template $domain missing $field" }
  }
  foreach ($field in $computationFields) {
    if ($templateText -notlike "*$field*") { throw "Domain template $domain missing computation field $field" }
  }

  Write-Output "Domain kernel binding OK: $domain"
}

Write-Output "Domain kernel binding validation passed for $($expectedDomains.Count) domain(s)."
