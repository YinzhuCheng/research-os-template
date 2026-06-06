param(
  [string]$ProfilesRoot = "domain_profiles"
)

$ErrorActionPreference = "Stop"

$expectedDomains = @(
  "fundamental-mathematics",
  "applied-mathematics",
  "machine-learning",
  "computer-science",
  "statistics"
)

$commonStatuses = @(
  "draft",
  "needs_human_review",
  "evidence_linked",
  "counterexample_or_failure_checked",
  "ready_for_public_export"
)

$requiredProfileFields = @(
  "domain_id:",
  "display_name:",
  "research_family:",
  "classification_sources:",
  "activation:",
  "paradigms:",
  "artifact_types:",
  "quality_gates:",
  "status_lifecycle:",
  "harness_boundaries:",
  "source_basis:"
)

if (!(Test-Path -LiteralPath $ProfilesRoot)) {
  throw "Domain profile root missing: $ProfilesRoot"
}

foreach ($domain in $expectedDomains) {
  $profile = Join-Path $ProfilesRoot "$domain\profile.yaml"
  $agents = Join-Path $ProfilesRoot "$domain\agents.yaml"
  if (!(Test-Path -LiteralPath $profile)) { throw "Missing domain profile: $profile" }
  if (!(Test-Path -LiteralPath $agents)) { throw "Missing agent registry: $agents" }

  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $profile
  foreach ($field in $requiredProfileFields) {
    if ($text -notlike "*$field*") { throw "Domain $domain missing profile field $field" }
  }
  if ($text -notmatch "domain_id:\s+$domain") { throw "Domain id mismatch in $profile" }
  foreach ($status in $commonStatuses) {
    if ($text -notlike "*$status*") { throw "Domain $domain missing lifecycle status $status" }
  }
  foreach ($boundary in @("PRIVATE/", "paid_resources: false", "external_write: forbidden_without_explicit_human_confirmation")) {
    if ($text -notlike "*$boundary*") { throw "Domain $domain missing harness boundary $boundary" }
  }
  if ($domain -eq "fundamental-mathematics") {
    foreach ($mathStatus in @("conjecture", "counterexample_found", "proof_sketch", "proof_gap", "human_checked", "formalization_future_slot")) {
      if ($text -notlike "*$mathStatus*") { throw "Math profile missing status $mathStatus" }
    }
    if ($text -notlike "*formalization_default: false*") {
      throw "Math profile must keep formalization disabled by default."
    }
  }
  if ($text -match "(?i)(authorization:\s*bearer|api[_-]?key\s*[:=]\s*['""][^'""]{8,}|password\s*[:=]\s*['""][^'""]{8,})") {
    throw "Domain profile $domain appears to contain a secret literal."
  }
  Write-Output "Domain profile OK: $domain"
}

Write-Output "Domain profile validation passed for $($expectedDomains.Count) domain(s)."
