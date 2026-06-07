param(
  [string]$PackagePath = ""
)

$ErrorActionPreference = "Stop"

$script = "scripts\package_template.ps1"
if (!(Test-Path -LiteralPath $script)) {
  throw "Missing package script: $script"
}

$text = Get-Content -Raw -Encoding UTF8 -LiteralPath $script
foreach ($blocked in @(".git", "build", "exports", "PRIVATE")) {
  if ($text -notlike "*$blocked*") {
    throw "Package script does not name forbidden path: $blocked"
  }
}
if ($text -notmatch '\$allowlist') {
  throw "Package script must use an explicit allowlist."
}

if ($PackagePath) {
  if (!(Test-Path -LiteralPath $PackagePath)) {
    throw "Package not found: $PackagePath"
  }
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $zip = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path -LiteralPath $PackagePath).Path)
  try {
    foreach ($entry in $zip.Entries) {
      $name = $entry.FullName -replace "\\", "/"
      foreach ($blocked in @(".git/", "build/", "exports/", "PRIVATE/")) {
        if ($name.StartsWith($blocked, [System.StringComparison]::OrdinalIgnoreCase)) {
          throw "Package contains forbidden path: $name"
        }
      }
    }
  } finally {
    $zip.Dispose()
  }
}

Write-Output "Package artifact check passed."
