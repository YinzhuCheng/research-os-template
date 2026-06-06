param(
  [string[]]$Paths = @("PUBLIC", "PROVENANCE"),
  [switch]$Quiet
)

$ErrorActionPreference = "Stop"

$patterns = @(
  @{Name="OpenAI-like secret"; Regex="sk-[A-Za-z0-9_-]{20,}"},
  @{Name="Authorization header"; Regex="(?i)authorization\s*:"},
  @{Name="Bearer token"; Regex="(?i)bearer\s+[A-Za-z0-9._-]{16,}"},
  @{Name="Cookie header"; Regex="(?i)cookie\s*:"},
  @{Name="API key assignment"; Regex="(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['""][^'""]{8,}['""]"}
)

$hits = @()
foreach ($path in $Paths) {
  if (!(Test-Path -LiteralPath $path)) { continue }
  Get-ChildItem -LiteralPath $path -Recurse -File | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content -Raw -LiteralPath $file -ErrorAction SilentlyContinue
    foreach ($pattern in $patterns) {
      if ($content -match $pattern.Regex) {
        $hits += [pscustomobject]@{
          Path = $file
          Rule = $pattern.Name
        }
      }
    }
  }
}

if ($hits.Count -gt 0) {
  if (!$Quiet) { $hits | Format-Table -AutoSize }
  throw "Privacy scan failed with $($hits.Count) hit(s)."
}

if (!$Quiet) { Write-Output "Privacy scan passed." }
