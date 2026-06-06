param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$statePath = Join-Path $Root "PUBLIC\copilot_state.json"
if (!(Test-Path -LiteralPath $statePath)) {
  throw "Missing sanitized copilot state: PUBLIC\copilot_state.json"
}

$raw = Get-Content -Raw -Encoding UTF8 -LiteralPath $statePath
$state = $raw | ConvertFrom-Json

foreach ($field in @("schema_version", "updated_at", "state", "overview", "literature", "theory", "experiment", "repository_links")) {
  if ($null -eq $state.$field) { throw "PUBLIC\copilot_state.json missing $field" }
}

if ($raw -match "PRIVATE[\\/]" -or $raw -match "private_runtime_path") {
  throw "Sanitized copilot state must not expose PRIVATE paths or private_runtime_path."
}

if ($state.literature.download_script -ne "scripts/download_reference_links.ps1") {
  throw "Copilot state must expose the reference download script path."
}

Write-Output "Copilot public state validation passed."
