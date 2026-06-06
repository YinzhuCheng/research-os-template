param(
  [string]$PythonPath = "",
  [switch]$RequireCodexPluginFiles,
  [switch]$RequireLatex
)

$ErrorActionPreference = "Stop"

function Find-CommandPath([string]$Name) {
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  return $null
}

function Get-PythonCommand([string]$Preferred) {
  if ($Preferred) { return $Preferred }
  $python = Find-CommandPath "python"
  if ($python) { return $python }
  $python3 = Find-CommandPath "python3"
  if ($python3) { return $python3 }
  return $null
}

function Require-File([string]$Path) {
  if (!(Test-Path -LiteralPath $Path)) { throw "Missing required file: $Path" }
}

$results = @()

$results += [pscustomobject]@{
  Check = "PowerShell"
  Status = "ok"
  Detail = $PSVersionTable.PSVersion.ToString()
}

$git = Find-CommandPath "git"
if (!$git) { throw "Git is required but was not found on PATH." }
$gitVersion = (& git --version) -join " "
$results += [pscustomobject]@{ Check = "Git"; Status = "ok"; Detail = $gitVersion }

$pythonCmd = Get-PythonCommand $PythonPath
if (!$pythonCmd) { throw "Python 3.10+ is required but was not found on PATH. Pass -PythonPath if needed." }
$pythonVersion = (& $pythonCmd --version 2>&1) -join " "
if ($pythonVersion -notmatch "Python\s+([0-9]+)\.([0-9]+)") {
  throw "Unable to parse Python version: $pythonVersion"
}
$major = [int]$Matches[1]
$minor = [int]$Matches[2]
if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
  throw "Python 3.10+ is required; found $pythonVersion"
}
$results += [pscustomobject]@{ Check = "Python"; Status = "ok"; Detail = $pythonVersion }

Require-File "PUBLIC\copilot.html"
Require-File "PUBLIC\index.html"
Require-File ".agents\plugins\plugins\research-os-copilot\scripts\research_os_copilot_server.py"
Require-File "scripts\download_reference_links.ps1"
Require-File "scripts\validate_schemas.ps1"
Require-File "scripts\validate_skills.ps1"
$results += [pscustomobject]@{ Check = "Repository files"; Status = "ok"; Detail = "Copilot, dashboard, scripts present" }

if ($RequireCodexPluginFiles) {
  Require-File ".agents\plugins\marketplace.json"
  Require-File ".agents\plugins\plugins\research-os-copilot\.codex-plugin\plugin.json"
  Require-File ".agents\plugins\plugins\research-os-copilot\.mcp.json"
  $results += [pscustomobject]@{ Check = "Codex plugin files"; Status = "ok"; Detail = "Repo-scoped plugin scaffold present" }
}

if ($RequireLatex) {
  $latex = Find-CommandPath "pdflatex"
  if (!$latex) { throw "LaTeX requested but pdflatex was not found on PATH." }
  $results += [pscustomobject]@{ Check = "LaTeX"; Status = "ok"; Detail = (& pdflatex --version | Select-Object -First 1) }
}

$results | Format-Table -AutoSize
Write-Output "Environment check passed. OS package names and install commands may need adjustment for your OS version."
