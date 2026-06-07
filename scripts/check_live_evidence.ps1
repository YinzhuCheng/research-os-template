param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$snapshotPath = Join-Path $Root "PROVENANCE\live_evidence_snapshot.yaml"
if (!(Test-Path -LiteralPath $snapshotPath)) {
  throw "Missing live evidence snapshot."
}

$text = Get-Content -Raw -Encoding UTF8 -LiteralPath $snapshotPath
foreach ($pattern in @("snapshot_id:\s+LE-", "source_url:\s+""?https?://", "accessed_at:\s+""?\d{4}-\d{2}-\d{2}""?", "freshness_risk:\s+(low|medium|high)")) {
  if ($text -notmatch $pattern) {
    throw "Live evidence check failed: missing $pattern"
  }
}

Write-Output "Live evidence check passed."
