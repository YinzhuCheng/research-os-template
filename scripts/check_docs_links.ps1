param(
  [string[]]$Roots = @("README.md", "docs", "PUBLIC")
)

$ErrorActionPreference = "Stop"

function Test-LocalLink([string]$SourceFile, [string]$Href) {
  if (!$Href) { return }
  if ($Href.StartsWith("#")) { return }
  if ($Href.StartsWith('$')) { return }
  if ($Href -match "^(https?|mailto|app):") { return }
  if ($Href -match "^\{") { return }

  $clean = ($Href -split "#")[0]
  if (!$clean) { return }
  $clean = [System.Uri]::UnescapeDataString($clean)
  $baseDir = Split-Path -Parent $SourceFile
  if (!$baseDir) { $baseDir = "." }
  $candidate = Join-Path $baseDir $clean
  if (!(Test-Path -LiteralPath $candidate)) {
    throw "Broken local link in ${SourceFile}: $Href -> $candidate"
  }
}

function Get-RelativePathCompat([string]$BasePath, [string]$TargetPath) {
  $baseFull = [System.IO.Path]::GetFullPath($BasePath).TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
  $targetFull = [System.IO.Path]::GetFullPath($TargetPath)
  $baseUri = [System.Uri]::new($baseFull)
  $targetUri = [System.Uri]::new($targetFull)
  [System.Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

$files = @()
foreach ($root in $Roots) {
  if (Test-Path -LiteralPath $root -PathType Leaf) {
    $files += Get-Item -LiteralPath $root
  } elseif (Test-Path -LiteralPath $root -PathType Container) {
    $files += Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
      $_.Extension -in @(".md", ".html")
    }
  }
}

foreach ($file in $files) {
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $file.FullName
  $source = Get-RelativePathCompat (Get-Location) $file.FullName
  $mdLinks = [regex]::Matches($text, "\[[^\]]+\]\(([^)]+)\)")
  foreach ($match in $mdLinks) { Test-LocalLink $source $match.Groups[1].Value }
  $htmlLinks = [regex]::Matches($text, "href\s*=\s*['""]([^'""]+)['""]", "IgnoreCase")
  foreach ($match in $htmlLinks) { Test-LocalLink $source $match.Groups[1].Value }
  Write-Output "Doc links OK: $source"
}

Write-Output "Documentation link check passed for $($files.Count) file(s)."
