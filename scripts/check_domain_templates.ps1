param(
  [string]$TemplateRoot = "templates\domain"
)

$ErrorActionPreference = "Stop"

$expectedTemplates = @{
  "fundamental-mathematics" = @{
    File = "math_discovery_case.template.yaml"
    Needles = @("conjecture_card:", "example_bank:", "counterexample_log:", "proof_strategy:", "proof_gap_report:", "theorem_note:")
  }
  "applied-mathematics" = @{
    File = "applied_math_model_case.template.yaml"
    Needles = @("model_assumption_ledger:", "nondimensionalization_note:", "stability_check:", "numerical_validation_plan:", "sensitivity_report:")
  }
  "machine-learning" = @{
    File = "ml_research_case.template.yaml"
    Needles = @("task_card:", "data_card:", "baseline_matrix:", "ablation_plan:", "leakage_audit:", "eval_harness_spec:")
  }
  "computer-science" = @{
    File = "cs_research_case.template.yaml"
    Needles = @("problem_spec:", "algorithm_invariant_note:", "complexity_argument:", "system_design_record:", "benchmark_protocol:", "artifact_eval_pack:")
  }
  "statistics" = @{
    File = "statistical_inference_case.template.yaml"
    Needles = @("estimand_card:", "identification_memo:", "sampling_power_plan:", "diagnostic_report:", "uncertainty_statement:", "sensitivity_analysis:")
  }
}

$kernelNeedles = @(
  "research_kernel:",
  "evaluator_contracts:",
  "metric_or_check:",
  "formula_or_procedure:",
  "acceptance_threshold:",
  "resource_estimate:",
  "failure_mode:",
  "replay_note:",
  "negative_result_policy:",
  "human_judgment_gate:"
)

foreach ($domain in $expectedTemplates.Keys) {
  $spec = $expectedTemplates[$domain]
  $path = Join-Path $TemplateRoot "$domain\$($spec.File)"
  if (!(Test-Path -LiteralPath $path)) { throw "Missing domain template: $path" }
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $path
  if ($text -notmatch "domain_id:\s+$domain") { throw "Template domain mismatch: $path" }
  foreach ($needle in $spec.Needles) {
    if ($text -notlike "*$needle*") { throw "Template $path missing $needle" }
  }
  foreach ($needle in $kernelNeedles) {
    if ($text -notlike "*$needle*") { throw "Template $path missing research kernel field $needle" }
  }
  Write-Output "Domain template OK: $domain"
}

Write-Output "Domain template validation passed for $($expectedTemplates.Count) domain(s)."
