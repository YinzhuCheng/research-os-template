param(
  [string]$ProfilesRoot = "domain_profiles"
)

$ErrorActionPreference = "Stop"

$expectedAgentCounts = @{
  "fundamental-mathematics" = 6
  "applied-mathematics" = 6
  "machine-learning" = 7
  "computer-science" = 6
  "statistics" = 6
}

$requiredAgentFields = @(
  "agent_id:",
  "role:",
  "inputs:",
  "outputs:",
  "allowed_paths:",
  "forbidden_paths:",
  "resource_policy:",
  "network_policy:",
  "external_write_policy:",
  "public_output_policy:"
)

foreach ($domain in $expectedAgentCounts.Keys) {
  $path = Join-Path $ProfilesRoot "$domain\agents.yaml"
  if (!(Test-Path -LiteralPath $path)) { throw "Missing agent registry: $path" }
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $path
  if ($text -notmatch "domain_id:\s+$domain") { throw "Agent registry domain mismatch: $domain" }

  $agentCount = ([regex]::Matches($text, "(?m)^\s+- agent_id:\s+[a-z0-9-]+")).Count
  if ($agentCount -lt $expectedAgentCounts[$domain]) {
    throw "Domain $domain expected at least $($expectedAgentCounts[$domain]) agents, found $agentCount."
  }
  foreach ($field in $requiredAgentFields) {
    if ($text -notlike "*$field*") { throw "Domain $domain agent registry missing $field" }
  }
  foreach ($policy in @("PRIVATE/", "paid_resources: false", "external_write_policy: forbidden_without_explicit_confirmation")) {
    if ($text -notlike "*$policy*") { throw "Domain $domain agent registry missing policy $policy" }
  }
  $externalWriteMatches = ([regex]::Matches($text, "external_write_policy:\s+forbidden_without_explicit_confirmation")).Count
  if ($externalWriteMatches -lt $agentCount) {
    throw "Domain $domain has an agent without strict external write policy."
  }
  if ($text -match "(?i)(authorization:\s*bearer|api[_-]?key\s*[:=]\s*['""][^'""]{8,}|password\s*[:=]\s*['""][^'""]{8,})") {
    throw "Agent registry $domain appears to contain a secret literal."
  }
  Write-Output "Agent capability OK: $domain ($agentCount agents)"
}

Write-Output "Agent capability validation passed."
