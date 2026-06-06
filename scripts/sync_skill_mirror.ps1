param(
  [string]$Source = "skills",
  [string]$Destination = ".agents\skills"
)

$ErrorActionPreference = "Stop"

function Get-AbsolutePath([string]$Path) {
  [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
}

$root = Get-AbsolutePath "."
$sourceFull = Get-AbsolutePath $Source
$destinationFull = Get-AbsolutePath $Destination

if (!(Test-Path -LiteralPath $sourceFull)) {
  throw "Source skill directory not found: $sourceFull"
}

if (!$destinationFull.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Refusing to sync outside repository: $destinationFull"
}

New-Item -ItemType Directory -Force -Path $destinationFull | Out-Null

$sourceSkills = Get-ChildItem -LiteralPath $sourceFull -Directory | Where-Object {
  Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

$expected = @{}
foreach ($skill in $sourceSkills) {
  $expected[$skill.Name] = $true
  $target = Join-Path $destinationFull $skill.Name
  $targetFull = [System.IO.Path]::GetFullPath($target)
  if (!$targetFull.StartsWith($destinationFull, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing unsafe mirror target: $targetFull"
  }
  if (Test-Path -LiteralPath $targetFull) {
    Remove-Item -LiteralPath $targetFull -Recurse -Force
  }
  Copy-Item -LiteralPath $skill.FullName -Destination $targetFull -Recurse
  Write-Output "Mirrored $($skill.Name) -> $targetFull"
}

Get-ChildItem -LiteralPath $destinationFull -Directory | ForEach-Object {
  if (!$expected.ContainsKey($_.Name)) {
    $extraFull = [System.IO.Path]::GetFullPath($_.FullName)
    if (!$extraFull.StartsWith($destinationFull, [System.StringComparison]::OrdinalIgnoreCase)) {
      throw "Refusing unsafe extra mirror path: $extraFull"
    }
    Remove-Item -LiteralPath $extraFull -Recurse -Force
    Write-Output "Removed stale mirror $($_.Name)"
  }
}

Write-Output "Skill mirror sync complete for $($sourceSkills.Count) skill(s)."
