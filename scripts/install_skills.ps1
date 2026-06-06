param(
  [string]$Source = "skills",
  [string]$Destination = "$HOME\.codex\skills"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $Source)) {
  throw "Source skill directory not found: $Source"
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

Get-ChildItem -LiteralPath $Source -Directory | ForEach-Object {
  $skillFile = Join-Path $_.FullName "SKILL.md"
  if (!(Test-Path -LiteralPath $skillFile)) {
    return
  }
  $target = Join-Path $Destination $_.Name
  if (Test-Path -LiteralPath $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
  }
  Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse
  Write-Output "Installed $($_.Name) -> $target"
}
