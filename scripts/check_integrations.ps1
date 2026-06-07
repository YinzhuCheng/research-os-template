param(
  [string]$Registry = "docs\integrations\components.yaml"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $Registry)) {
  throw "Integration registry missing: $Registry"
}
foreach ($required in @("config\schemas\adapter_contract.schema.json", "templates\adapters\adapter_contract.template.yaml", "adapters\README.md")) {
  if (!(Test-Path -LiteralPath $required)) {
    throw "Missing adapter contract artifact: $required"
  }
}

$text = Get-Content -Raw -Encoding UTF8 -LiteralPath $Registry
$requiredTop = @("registry_id:", "updated_at:", "default_policy:", "components:")
foreach ($item in $requiredTop) {
  if ($text -notlike "*$item*") { throw "Integration registry missing $item" }
}

$componentBlocks = [regex]::Matches($text, "(?ms)^  - id:\s+.+?(?=^  - id:|\z)")
if ($componentBlocks.Count -lt 7) {
  throw "Expected at least 7 integration components, found $($componentBlocks.Count)."
}

$requiredFields = @(
  "name:",
  "source_url:",
  "license:",
  "accessed_at:",
  "adapter_status:",
  "research_os_phases:",
  "install_reference:",
  "credential_env_vars:",
  "inputs:",
  "outputs:",
  "artifact_mapping:",
  "risks:",
  "sandbox:",
  "cost:",
  "privacy:",
  "external_write:"
)

foreach ($match in $componentBlocks) {
  $block = $match.Value
  $idMatch = [regex]::Match($block, "id:\s+([a-z0-9-]+)")
  if (!$idMatch.Success) { throw "Component block missing id." }
  $id = $idMatch.Groups[1].Value
  foreach ($field in $requiredFields) {
    if ($block -notlike "*$field*") {
      throw "Component $id missing $field"
    }
  }
  if ($block -match "(?i)(authorization:\s*bearer|api[_-]?key\s*[:=]\s*['""][^'""]{8,}|password\s*[:=]\s*['""][^'""]{8,})") {
    throw "Component $id appears to contain a secret literal."
  }
  Write-Output "Integration component OK: $id"
}

Write-Output "Integration registry validation passed for $($componentBlocks.Count) component(s)."
