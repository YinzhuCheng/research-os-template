param(
  [string]$Source = "skills",
  [string]$Mirror = ".agents\skills"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $Source)) { throw "Source skills missing: $Source" }
if (!(Test-Path -LiteralPath $Mirror)) { throw "Mirror skills missing: $Mirror" }

function Get-RelativePathCompat([string]$BasePath, [string]$TargetPath) {
  $baseFull = [System.IO.Path]::GetFullPath($BasePath).TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
  $targetFull = [System.IO.Path]::GetFullPath($TargetPath)
  $baseUri = [System.Uri]::new($baseFull)
  $targetUri = [System.Uri]::new($targetFull)
  [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

$sourceSkills = Get-ChildItem -LiteralPath $Source -Directory | Where-Object {
  Test-Path -LiteralPath (Join-Path $_.FullName "SKILL.md")
}

if ($sourceSkills.Count -eq 0) { throw "No source skills found." }

foreach ($skill in $sourceSkills) {
  $mirrorSkill = Join-Path $Mirror $skill.Name
  $mirrorSkillFile = Join-Path $mirrorSkill "SKILL.md"
  if (!(Test-Path -LiteralPath $mirrorSkillFile)) {
    throw "Missing mirrored skill: $($skill.Name)"
  }

  $sourceFiles = Get-ChildItem -LiteralPath $skill.FullName -Recurse -File | Where-Object {
    $_.FullName -notmatch "__pycache__"
  }
  foreach ($sourceFile in $sourceFiles) {
    $relative = Get-RelativePathCompat $skill.FullName $sourceFile.FullName
    $mirrorFile = Join-Path $mirrorSkill $relative
    if (!(Test-Path -LiteralPath $mirrorFile)) {
      throw "Missing mirrored file: $($skill.Name)\$relative"
    }
    $sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourceFile.FullName).Hash
    $mirrorHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $mirrorFile).Hash
    if ($sourceHash -ne $mirrorHash) {
      throw "Mirror mismatch: $($skill.Name)\$relative"
    }
  }
  Write-Output "Skill mirror OK: $($skill.Name)"
}

$mirrorSkills = Get-ChildItem -LiteralPath $Mirror -Directory
foreach ($mirrorSkill in $mirrorSkills) {
  if (!($sourceSkills.Name -contains $mirrorSkill.Name)) {
    throw "Stale mirrored skill: $($mirrorSkill.Name)"
  }
}

Write-Output "Skill mirror validation passed for $($sourceSkills.Count) skill(s)."
