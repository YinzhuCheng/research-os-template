param()

$ErrorActionPreference = "Stop"

function Require-File([string]$Path) {
  if (!(Test-Path -LiteralPath $Path)) { throw "Missing required file: $Path" }
}

function Require-Text([string]$Path, [string]$Needle) {
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $Path
  if ($text -notlike "*$Needle*") {
    throw "Missing '$Needle' in $Path"
  }
}

Require-File "docs\environment.md"
Require-File "scripts\install_environment.ps1"
Require-File "scripts\check_environment.ps1"
Require-File "scripts\check_latex_sources.ps1"

Require-Text "README.md" "docs/environment.md"
Require-Text "docs\README.md" "environment.md"
Require-Text "docs\doc_map.yaml" "scripts/install_environment.ps1"
Require-Text "docs\doc_map.yaml" "scripts/check_environment.ps1"
Require-Text "PUBLIC\dashboard_data.json" "../docs/environment.md"
Require-Text "PUBLIC\index.html" "../docs/environment.md"
Require-Text "docs\technical-report.html" "scripts/install_environment.ps1"
Require-Text "docs\start-here.html" "scripts\install_environment.ps1"

$dashboard = Get-Content -Raw -Encoding UTF8 -LiteralPath "PUBLIC\dashboard_data.json" | ConvertFrom-Json
$requiredPaths = @(
  "../docs/environment.md",
  "../scripts/install_environment.ps1",
  "../scripts/check_environment.ps1"
)
foreach ($path in $requiredPaths) {
  if (!($dashboard.documents.path -contains $path)) {
    throw "Dashboard data missing environment path: $path"
  }
}

Write-Output "Environment documentation check passed."
