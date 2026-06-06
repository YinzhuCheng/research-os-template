param(
  [string]$SkillsDir = "skills"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $SkillsDir)) {
  throw "Skills directory missing: $SkillsDir"
}

$skills = Get-ChildItem -LiteralPath $SkillsDir -Directory
if ($skills.Count -eq 0) {
  throw "No skills found."
}

foreach ($skill in $skills) {
  $skillFile = Join-Path $skill.FullName "SKILL.md"
  if (!(Test-Path -LiteralPath $skillFile)) {
    throw "Missing SKILL.md: $($skill.Name)"
  }
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $skillFile
  if ($text -notmatch "(?s)^---\s*name:\s*$($skill.Name)\s*description:\s+.+?---") {
    throw "Invalid frontmatter in $($skill.Name)"
  }
  if (!(Test-Path -LiteralPath (Join-Path $skill.FullName "references"))) {
    throw "Missing references directory: $($skill.Name)"
  }
  if (!(Test-Path -LiteralPath (Join-Path $skill.FullName "assets"))) {
    throw "Missing assets directory: $($skill.Name)"
  }
  Write-Output "Skill OK: $($skill.Name)"
}

Write-Output "Skill validation passed for $($skills.Count) skill(s)."
