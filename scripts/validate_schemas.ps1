param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Require-File([string]$Path) {
  if (!(Test-Path -LiteralPath $Path)) {
    throw "Required file missing: $Path"
  }
}

function Require-Text([string]$Path, [string]$Pattern) {
  $text = Get-Content -Raw -LiteralPath $Path
  if ($text -notmatch $Pattern) {
    throw "Required pattern missing in ${Path}: $Pattern"
  }
}

$schemaDir = Join-Path $Root "config\schemas"
Require-File (Join-Path $Root "config\research_project.yaml")
Require-File (Join-Path $Root "CONTROL\work_order.yaml")
Require-File (Join-Path $Root "PUBLIC\claim_evidence_matrix.yaml")
Require-File (Join-Path $Root "PROVENANCE\run_manifest.jsonl")

Get-ChildItem -LiteralPath $schemaDir -Filter "*.json" | ForEach-Object {
  Get-Content -Raw -LiteralPath $_.FullName | ConvertFrom-Json | Out-Null
  Write-Output "JSON schema OK: $($_.Name)"
}

Require-Text (Join-Path $Root "config\research_project.yaml") "language_mode:\s+(zh-first|en-only)"
Require-Text (Join-Path $Root "config\research_project.yaml") "intervention_level:\s+(low|medium|high)"
Require-Text (Join-Path $Root "CONTROL\work_order.yaml") "work_order_id:\s+WO-[0-9]{4}"
Require-Text (Join-Path $Root "PUBLIC\claim_evidence_matrix.yaml") "CLAIM-[0-9]{3}"

Get-Content -LiteralPath (Join-Path $Root "PROVENANCE\run_manifest.jsonl") | ForEach-Object {
  if ($_.Trim()) {
    $_ | ConvertFrom-Json | Out-Null
  }
}

Write-Output "Research OS schema smoke validation passed."
