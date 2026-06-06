param(
  [string[]]$Paths = @("PUBLIC", "CONTROL", "PROVENANCE"),
  [string]$OutFile = "PROVENANCE\hashes.json"
)

$ErrorActionPreference = "Stop"
$records = @()
$outFull = if (Test-Path -LiteralPath $OutFile) { (Resolve-Path -LiteralPath $OutFile).Path } else { (Join-Path (Get-Location) $OutFile) }

foreach ($path in $Paths) {
  if (!(Test-Path -LiteralPath $path)) { continue }
  Get-ChildItem -LiteralPath $path -Recurse -File | Sort-Object FullName | ForEach-Object {
    if ($_.FullName -eq $outFull) { return }
    $hash = Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256
    $records += [pscustomobject]@{
      path = (Resolve-Path -LiteralPath $_.FullName -Relative)
      sha256 = $hash.Hash.ToLowerInvariant()
      bytes = $_.Length
    }
  }
}

$json = $records | ConvertTo-Json -Depth 4
Set-Content -LiteralPath $OutFile -Value $json -Encoding UTF8
Write-Output "Wrote $OutFile"
