param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$configPath = Join-Path $Root "config\research_project.yaml"
$ledgerPath = Join-Path $Root "PROVENANCE\resource_ledger.jsonl"

if (!(Test-Path -LiteralPath $configPath)) { throw "Missing config." }
if (!(Test-Path -LiteralPath $ledgerPath)) { throw "Missing resource ledger." }

$config = Get-Content -Raw -Encoding UTF8 -LiteralPath $configPath
if ($config -notmatch "resource_budget\s*:") { throw "Missing resource_budget." }
if ($config -match "model_budget\s*:") { throw "Forbidden model_budget remains." }

foreach ($category in @("time", "compute", "cloud", "lab", "material", "api", "model", "human", "other")) {
  if ($config -notmatch "(?m)^\s+$category\s*:") {
    throw "Missing resource category: $category"
  }
}

Get-Content -LiteralPath $ledgerPath | ForEach-Object {
  if ($_.Trim()) {
    $entry = $_ | ConvertFrom-Json
    foreach ($field in @("entry_id", "work_order_id", "resource_type", "amount", "currency_or_unit", "status", "privacy_level")) {
      if (-not $entry.PSObject.Properties.Name.Contains($field)) {
        throw "Resource ledger entry missing field: $field"
      }
    }
  }
}

$simulatedResources = @("api", "cloud", "material", "human")
foreach ($resource in $simulatedResources) {
  if ($config -notmatch "(?m)^\s+$resource\s*:") {
    throw "Resource guard cannot represent simulated resource: $resource"
  }
}

Write-Output "Resource guard check passed."
