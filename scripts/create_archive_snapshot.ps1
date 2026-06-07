param(
  [Parameter(Mandatory=$true)]
  [string]$Description,
  [string]$MacroPhase = "unknown",
  [string]$ArchiveId = "",
  [switch]$Preview
)

$ErrorActionPreference = "Stop"

function Invoke-Git([string[]]$Args) {
  $output = & git @Args 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "git $($Args -join ' ') failed: $output"
  }
  $output
}

function Get-RepoRoot {
  $root = Invoke-Git @("rev-parse", "--show-toplevel")
  [string]$root.Trim()
}

function Get-ChangedPaths {
  $lines = Invoke-Git @("status", "--porcelain")
  $paths = @()
  foreach ($line in $lines) {
    if (!$line.Trim()) { continue }
    $path = $line.Substring(3).Trim() -replace "\\", "/"
    if ($path -like "* -> *") { $path = ($path -split " -> ")[1] }
    $paths += $path
  }
  $paths
}

function Assert-ArchiveSafe([string]$Root, [string[]]$Paths) {
  foreach ($path in $Paths) {
    if ($path -like "PRIVATE/*" -or $path -like "*/PRIVATE/*") {
      throw "Archive refuses PRIVATE path: $path"
    }
    $full = Join-Path $Root $path
    if (Test-Path -LiteralPath $full -PathType Leaf) {
      $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $full -ErrorAction SilentlyContinue
      if ($text -match "(?i)(authorization\s*:|bearer\s+[a-z0-9._-]{12,}|api[_-]?key|secret[_-]?key|cookie\s*:|token\s*[:=])") {
        throw "Archive secrets scan failed for changed path: $path"
      }
    }
  }
}

function Read-YamlValue([string]$Path, [string]$Key, [string]$Default) {
  if (!(Test-Path -LiteralPath $Path)) { return $Default }
  foreach ($line in Get-Content -Encoding UTF8 -LiteralPath $Path) {
    if ($line -match "^$([regex]::Escape($Key)):\s*(.+)$") {
      return $Matches[1].Trim().Trim('"')
    }
  }
  $Default
}

$root = Get-RepoRoot
Set-Location $root

if (!$Description.Trim()) { throw "Archive description is required." }
if (!$ArchiveId) { $ArchiveId = "ARCH-" + (Get-Date -Format "yyyyMMdd-HHmmss") }
if ($ArchiveId -notmatch "^ARCH-[0-9A-Za-z_-]+$") { throw "Invalid ArchiveId: $ArchiveId" }
if ($MacroPhase -notin @("initialization", "research_loop", "final_product", "unknown")) { $MacroPhase = "unknown" }

$changed = @(Get-ChangedPaths)
Assert-ArchiveSafe $root $changed
$phase = Read-YamlValue (Join-Path $root "config\research_project.yaml") "current_phase" "unknown"
$branch = (Invoke-Git @("rev-parse", "--abbrev-ref", "HEAD")).Trim()
$head = (Invoke-Git @("rev-parse", "HEAD")).Trim()

if ($Preview) {
  [pscustomobject]@{
    ok = $true
    archive_id = $ArchiveId
    phase = $phase
    macro_phase = $MacroPhase
    git_branch = $branch
    git_commit = $head
    dirty = [bool]$changed.Count
    changed_paths = $changed
    private_paths_included = $false
    secrets_scan = "passed"
    status = "preview"
  } | ConvertTo-Json -Depth 8
  exit 0
}

if ($changed.Count -gt 0) {
  Invoke-Git @("add", "--all", "--", ".") | Out-Null
  Invoke-Git @("-c", "user.name=Research OS Archive", "-c", "user.email=research-os-archive@example.invalid", "commit", "-m", "archive snapshot: $($Description.Substring(0, [Math]::Min(72, $Description.Length)))") | Out-Null
  $head = (Invoke-Git @("rev-parse", "HEAD")).Trim()
}

$record = [ordered]@{
  archive_id = $ArchiveId
  created_at = (Get-Date).ToString("o")
  phase = $phase
  macro_phase = $MacroPhase
  git_commit = $head
  git_branch = $branch
  description = $Description
  user_free_form = ""
  changed_paths = $changed
  public_index_path = "PUBLIC/archive_index.json"
  private_paths_included = $false
  secrets_scan = "passed"
  status = "created"
}

$archiveLog = Join-Path $root "PROVENANCE\archive_index.jsonl"
$publicIndex = Join-Path $root "PUBLIC\archive_index.json"
if (!(Test-Path -LiteralPath (Split-Path -Parent $archiveLog))) { New-Item -ItemType Directory -Path (Split-Path -Parent $archiveLog) | Out-Null }
if (!(Test-Path -LiteralPath (Split-Path -Parent $publicIndex))) { New-Item -ItemType Directory -Path (Split-Path -Parent $publicIndex) | Out-Null }
($record | ConvertTo-Json -Compress -Depth 8) + "`n" | Add-Content -Encoding UTF8 -LiteralPath $archiveLog

$archives = @()
Get-Content -Encoding UTF8 -LiteralPath $archiveLog | ForEach-Object {
  if ($_.Trim()) { $archives += ($_ | ConvertFrom-Json) }
}
$publicArchives = $archives | ForEach-Object {
  [ordered]@{
    archive_id = $_.archive_id
    created_at = $_.created_at
    phase = $_.phase
    macro_phase = $_.macro_phase
    git_commit = $_.git_commit
    git_branch = $_.git_branch
    description = $_.description
    changed_path_count = @($_.changed_paths).Count
    status = $_.status
  }
}
[ordered]@{ archives = $publicArchives } | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -LiteralPath $publicIndex

Invoke-Git @("add", "--", "PROVENANCE/archive_index.jsonl", "PUBLIC/archive_index.json") | Out-Null
Invoke-Git @("-c", "user.name=Research OS Archive", "-c", "user.email=research-os-archive@example.invalid", "commit", "-m", "archive index: $ArchiveId") | Out-Null
$record.index_commit = (Invoke-Git @("rev-parse", "HEAD")).Trim()

$record | ConvertTo-Json -Depth 8
