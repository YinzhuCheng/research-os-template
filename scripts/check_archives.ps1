param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Require-File([string]$Path) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Missing archive file: $Path" }
}

function Require-Text([string]$Path, [string]$Pattern) {
  $full = Join-Path $Root $Path
  Require-File $Path
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $full
  if ($text -notmatch $Pattern) { throw "Archive check failed: $Path missing $Pattern" }
}

Require-File "config\schemas\archive_record.schema.json"
Require-File "templates\yaml\archive_record.template.yaml"
Require-File "scripts\create_archive_snapshot.ps1"
Require-File "PUBLIC\archive_index.json"
Require-Text ".agents\plugins\plugins\research-os-copilot\scripts\research_os_copilot_server.py" "/api/archive-preview"
Require-Text ".agents\plugins\plugins\research-os-copilot\scripts\research_os_copilot_server.py" "/api/archive-snapshot"
Require-Text ".agents\plugins\plugins\research-os-copilot\scripts\research_os_copilot_server.py" "archive_index.jsonl"
Require-Text "scripts\create_archive_snapshot.ps1" "git"
Require-Text "scripts\create_archive_snapshot.ps1" "PRIVATE"
Require-Text "scripts\create_archive_snapshot.ps1" "secrets_scan"

Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "config\schemas\archive_record.schema.json") | ConvertFrom-Json | Out-Null
$public = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "PUBLIC\archive_index.json") | ConvertFrom-Json
if ($null -eq $public.archives) { throw "PUBLIC/archive_index.json must contain archives array." }

$archiveLog = Join-Path $Root "PROVENANCE\archive_index.jsonl"
if (Test-Path -LiteralPath $archiveLog) {
  Get-Content -Encoding UTF8 -LiteralPath $archiveLog | ForEach-Object {
    if ($_.Trim()) {
      $record = $_ | ConvertFrom-Json
      if ($record.private_paths_included -ne $false) { throw "Archive record includes private paths." }
      if ($record.description.Length -lt 1) { throw "Archive record missing description." }
    }
  }
}

Write-Output "Archive validation passed."
