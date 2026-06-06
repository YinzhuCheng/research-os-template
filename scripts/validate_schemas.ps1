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
Require-File (Join-Path $Root "config\research_flow.yaml")
Require-File (Join-Path $Root "CONTROL\work_order.yaml")
Require-File (Join-Path $Root "PUBLIC\claim_evidence_matrix.yaml")
Require-File (Join-Path $Root "PROVENANCE\run_manifest.jsonl")
Require-File (Join-Path $Root "PROVENANCE\resource_ledger.jsonl")
Require-File (Join-Path $Root "PROVENANCE\live_evidence_snapshot.yaml")
Require-File (Join-Path $Root "docs\doc_map.yaml")
Require-File (Join-Path $Root "docs\integrations\components.yaml")
Require-File (Join-Path $Root "templates\yaml\integration_component.template.yaml")
Require-File (Join-Path $Root "templates\yaml\harness_run.template.yaml")
Require-File (Join-Path $Root "templates\yaml\domain_profile.template.yaml")
Require-File (Join-Path $Root "templates\yaml\agent_capability.template.yaml")
Require-File (Join-Path $Root "templates\yaml\research_kernel.template.yaml")
Require-File (Join-Path $Root "templates\yaml\copilot_intake.template.yaml")
Require-File (Join-Path $Root "templates\yaml\copilot_questions.template.yaml")
Require-File (Join-Path $Root "templates\yaml\copilot_initialization_report.template.yaml")
Require-File (Join-Path $Root "templates\research_kernel\research_cycle.template.yaml")
Require-File (Join-Path $Root "domain_profiles\README.md")
Require-File (Join-Path $Root "domain_profiles\fundamental-mathematics\profile.yaml")
Require-File (Join-Path $Root "domain_profiles\applied-mathematics\profile.yaml")
Require-File (Join-Path $Root "domain_profiles\machine-learning\profile.yaml")
Require-File (Join-Path $Root "domain_profiles\computer-science\profile.yaml")
Require-File (Join-Path $Root "domain_profiles\statistics\profile.yaml")

Get-ChildItem -LiteralPath $schemaDir -Filter "*.json" | ForEach-Object {
  Get-Content -Raw -LiteralPath $_.FullName | ConvertFrom-Json | Out-Null
  Write-Output "JSON schema OK: $($_.Name)"
}

Require-Text (Join-Path $Root "config\research_project.yaml") "language_mode:\s+(zh-first|en-only)"
Require-Text (Join-Path $Root "config\research_project.yaml") "intervention_level:\s+(low|medium|high)"
Require-Text (Join-Path $Root "config\research_project.yaml") "resource_budget:\s*"
Require-Text (Join-Path $Root "config\research_project.yaml") "dissemination:\s*"
Require-Text (Join-Path $Root "config\research_project.yaml") "feasibility_probe:\s*"
Require-Text (Join-Path $Root "config\research_flow.yaml") "flow_id:\s+RESEARCH-FLOW-[0-9]{4}"
Require-Text (Join-Path $Root "config\research_flow.yaml") "canonical_sequence:\s*"
Require-Text (Join-Path $Root "config\research_flow.yaml") "material_intake"
Require-Text (Join-Path $Root "config\research_flow.yaml") "research_kernel"
Require-Text (Join-Path $Root "config\research_flow.yaml") "execution_harness"
Require-Text (Join-Path $Root "CONTROL\work_order.yaml") "work_order_id:\s+WO-[0-9]{4}"
Require-Text (Join-Path $Root "CONTROL\work_order.yaml") "resource_budget:\s*"
Require-Text (Join-Path $Root "PUBLIC\claim_evidence_matrix.yaml") "CLAIM-[0-9]{3}"
Require-Text (Join-Path $Root "docs\doc_map.yaml") "doc_map_id:\s+DOCMAP-[0-9]{4}"
Require-Text (Join-Path $Root "docs\doc_map.yaml") "domain_profiles"
Require-Text (Join-Path $Root "docs\doc_map.yaml") "research_kernel"
Require-Text (Join-Path $Root "docs\doc_map.yaml") "copilot"
Require-Text (Join-Path $Root "docs\doc_map.yaml") "process_contract"
Require-Text (Join-Path $Root "docs\integrations\components.yaml") "registry_id:\s+INTEGRATIONS-[0-9]{4}"
Require-Text (Join-Path $Root "config\schemas\copilot_intake.schema.json") "uploaded_files"
Require-Text (Join-Path $Root "config\schemas\copilot_questions.schema.json") "recommended_answer"
Require-Text (Join-Path $Root "config\schemas\copilot_questions.schema.json") "free_text_other"
Require-Text (Join-Path $Root "config\schemas\copilot_initialization_report.schema.json") "minimum_validation"

Get-Content -LiteralPath (Join-Path $Root "PROVENANCE\run_manifest.jsonl") | ForEach-Object {
  if ($_.Trim()) {
    $_ | ConvertFrom-Json | Out-Null
  }
}

Get-Content -LiteralPath (Join-Path $Root "PROVENANCE\resource_ledger.jsonl") | ForEach-Object {
  if ($_.Trim()) {
    $_ | ConvertFrom-Json | Out-Null
  }
}

Write-Output "Research OS schema smoke validation passed."
