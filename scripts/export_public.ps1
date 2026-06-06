param(
  [string]$OutDir = "exports",
  [string]$Name = ""
)

$ErrorActionPreference = "Stop"

& "$PSScriptRoot\scan_privacy.ps1" -Paths @("PUBLIC", "PROVENANCE")

if (!$Name) {
  $Name = "public_export_" + (Get-Date -Format "yyyyMMdd_HHmmss")
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$zipPath = Join-Path $OutDir "$Name.zip"
$stage = Join-Path $OutDir ".stage_$Name"

$resolvedOut = (Resolve-Path -LiteralPath $OutDir).Path
New-Item -ItemType Directory -Force -Path $stage | Out-Null
$resolvedStage = (Resolve-Path -LiteralPath $stage).Path
if (!$resolvedStage.StartsWith($resolvedOut)) {
  throw "Refusing to stage export outside $resolvedOut"
}

Copy-Item -LiteralPath "PUBLIC" -Destination (Join-Path $stage "PUBLIC") -Recurse
Copy-Item -LiteralPath "PROVENANCE" -Destination (Join-Path $stage "PROVENANCE") -Recurse

if (Test-Path -LiteralPath $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}
Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zipPath

Remove-Item -LiteralPath $stage -Recurse -Force
Write-Output "Wrote $zipPath"
