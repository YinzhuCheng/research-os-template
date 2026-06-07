param(
  [string]$OutDir = "exports",
  [string]$Name = "",
  [switch]$DryRun,
  [switch]$RemoveStage
)

$ErrorActionPreference = "Stop"

$forbidden = @(".git", "build", "exports", "PRIVATE", ".cache", ".codex_state", "__pycache__")
$allowlist = @(
  ".agents",
  ".codex",
  ".github",
  "adapters",
  "AGENTS.md",
  "config",
  "CONTROL",
  "docs",
  "domain_profiles",
  "evals",
  "PLAN",
  "PROVENANCE",
  "PUBLIC",
  "README.md",
  "RUNS",
  "scripts",
  "skills",
  "templates",
  "tests",
  "tools"
)

if (!$Name) {
  $Name = "research_os_template_" + (Get-Date -Format "yyyyMMdd_HHmmss")
}

& "$PSScriptRoot\scan_privacy.ps1" -Paths @("PUBLIC", "PROVENANCE")
& "$PSScriptRoot\check_strict_schema_instances.ps1"
& "$PSScriptRoot\check_public_summaries.ps1"
& "$PSScriptRoot\check_html_docs.ps1"
& "$PSScriptRoot\check_package_artifacts.ps1"

$included = @()
foreach ($item in $allowlist) {
  if (Test-Path -LiteralPath $item) {
    $included += $item
  }
}

if ($DryRun) {
  [pscustomobject]@{
    name = $Name
    included = $included
    forbidden = $forbidden
    dry_run = $true
  } | ConvertTo-Json -Depth 5
  return
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$stage = Join-Path $OutDir ".stage_$Name"
$zipPath = Join-Path $OutDir "$Name.zip"
New-Item -ItemType Directory -Force -Path $stage | Out-Null

foreach ($item in $included) {
  $target = Join-Path $stage $item
  $parent = Split-Path -Parent $target
  if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
  Copy-Item -LiteralPath $item -Destination $target -Recurse -Force
}

foreach ($blocked in $forbidden) {
  if (Test-Path -LiteralPath (Join-Path $stage $blocked)) {
    throw "Packaging stage contains forbidden path: $blocked"
  }
}

if (Test-Path -LiteralPath $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}
Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zipPath

if ($RemoveStage) {
  Remove-Item -LiteralPath $stage -Recurse -Force
}

Write-Output "Wrote $zipPath"
Write-Output "Stage retained at $stage unless -RemoveStage is used."
