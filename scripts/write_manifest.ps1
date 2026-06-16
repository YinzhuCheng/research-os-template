param(
  [string]$RunId = "RUN-0002",
  [string]$WorkOrderId = "WO-0001",
  [string]$Status = "planned",
  [string]$CommandOrTool = "codex",
  [string[]]$Inputs = @(),
  [string[]]$Outputs = @(),
  [string]$PrivacyLevel = "public",
  [string]$ManifestPath = "PROVENANCE\run_manifest.jsonl",
  [switch]$AllowCustomManifestPath
)

$ErrorActionPreference = "Stop"

function Hash-Map([string[]]$Items) {
  $map = @{}
  foreach ($item in $Items) {
    if (Test-Path -LiteralPath $item -PathType Leaf) {
      $map[$item] = (Get-FileHash -LiteralPath $item -Algorithm SHA256).Hash.ToLowerInvariant()
    }
  }
  return $map
}

function Resolve-RepoPath([string]$Path) {
  if ([System.IO.Path]::IsPathRooted($Path)) {
    return [System.IO.Path]::GetFullPath($Path)
  }
  return [System.IO.Path]::GetFullPath((Join-Path (Get-Location).Path $Path))
}

$defaultManifest = Resolve-RepoPath "PROVENANCE\run_manifest.jsonl"
$resolvedManifest = Resolve-RepoPath $ManifestPath
if (!$AllowCustomManifestPath -and $resolvedManifest -ne $defaultManifest) {
  throw "Refusing to write manifest outside PROVENANCE\run_manifest.jsonl without -AllowCustomManifestPath: $ManifestPath"
}

$manifestParent = Split-Path -Parent $resolvedManifest
if (!(Test-Path -LiteralPath $manifestParent)) {
  New-Item -ItemType Directory -Force -Path $manifestParent | Out-Null
}

$entry = [ordered]@{
  run_id = $RunId
  timestamp = (Get-Date).ToString("o")
  work_order_id = $WorkOrderId
  status = $Status
  command_or_tool = $CommandOrTool
  inputs = $Inputs
  outputs = $Outputs
  input_hashes = Hash-Map $Inputs
  output_hashes = Hash-Map $Outputs
  cost = @{ currency = "CNY"; estimated = 0 }
  errors = @()
  privacy_level = $PrivacyLevel
}

$json = $entry | ConvertTo-Json -Compress -Depth 6
Add-Content -LiteralPath $resolvedManifest -Value $json -Encoding UTF8
Write-Output "Appended manifest entry $RunId"
