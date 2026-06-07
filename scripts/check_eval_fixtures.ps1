param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$required = @(
  "evals\README.md",
  "evals\fixtures\schema_regression_case\README.md",
  "evals\fixtures\privacy_leak_case\README.md",
  "evals\fixtures\failed_experiment_replay\README.md",
  "evals\rubrics\research_os_regression_rubric.md",
  "evals\run_eval.py",
  "RUNS\experiments\EXP-0001\run.yaml",
  "PUBLIC\run_monitor.json"
)

foreach ($path in $required) {
  $full = Join-Path $Root $path
  if (!(Test-Path -LiteralPath $full)) {
    throw "Missing eval fixture artifact: $path"
  }
}

$monitor = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "PUBLIC\run_monitor.json") | ConvertFrom-Json
if (!$monitor.runs -or $monitor.runs.Count -lt 1) {
  throw "Run monitor must contain at least one sanitized run summary."
}
if (($monitor | ConvertTo-Json -Depth 8) -match "PRIVATE[\\/]|authorization:|bearer\s+") {
  throw "Run monitor contains private path or credential-like text."
}

Write-Output "Research OS eval fixtures check passed."
