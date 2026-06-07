param(
  [string]$PythonPath = "",
  [switch]$RequireTauriBuild
)

$ErrorActionPreference = "Stop"

function Find-CommandPath([string]$Name) {
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }
  return $null
}

function Get-PythonCandidates([string]$Preferred) {
  $candidates = @()
  if ($Preferred) { $candidates += [pscustomobject]@{ Exe = $Preferred; Args = @(); Label = $Preferred } }
  if ($env:RESEARCH_OS_PYTHON) { $candidates += [pscustomobject]@{ Exe = $env:RESEARCH_OS_PYTHON; Args = @(); Label = $env:RESEARCH_OS_PYTHON } }

  foreach ($name in @("python", "python3")) {
    $path = Find-CommandPath $name
    if ($path) { $candidates += [pscustomobject]@{ Exe = $path; Args = @(); Label = $path } }
  }

  $py = Find-CommandPath "py"
  if ($py) { $candidates += [pscustomobject]@{ Exe = $py; Args = @("-3"); Label = "$py -3" } }

  $codexPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
  if (Test-Path -LiteralPath $codexPython) { $candidates += [pscustomobject]@{ Exe = $codexPython; Args = @(); Label = $codexPython } }

  return $candidates
}

function Invoke-PythonVersion($Candidate) {
  $args = @($Candidate.Args) + @("--version")
  return (& $Candidate.Exe @args 2>&1) -join " "
}

function Require-File([string]$Path) {
  if (!(Test-Path -LiteralPath $Path)) { throw "Missing required file: $Path" }
}

$results = @()
$results += [pscustomobject]@{ Check = "PowerShell"; Status = "ok"; Detail = $PSVersionTable.PSVersion.ToString() }

$git = Find-CommandPath "git"
if (!$git) { throw "Git is required but was not found on PATH." }
$results += [pscustomobject]@{ Check = "Git"; Status = "ok"; Detail = ((& git --version) -join " ") }

$pythonCmd = $null
$pythonVersion = $null
foreach ($candidate in Get-PythonCandidates $PythonPath) {
  $candidateVersion = Invoke-PythonVersion $candidate
  if ($candidateVersion -match "Python\s+([0-9]+)\.([0-9]+)") {
    $pythonCmd = $candidate.Label
    $pythonVersion = $candidateVersion
    break
  }
}
if (!$pythonCmd) { throw "Python 3.10+ is required but no usable Python command was found. Pass -PythonPath if needed." }
if ([int]$Matches[1] -lt 3 -or ([int]$Matches[1] -eq 3 -and [int]$Matches[2] -lt 10)) {
  throw "Python 3.10+ is required; found $pythonVersion"
}
$results += [pscustomobject]@{ Check = "Python"; Status = "ok"; Detail = $pythonVersion }

Require-File "apps\research-os-desktop\package.json"
Require-File "apps\research-os-sidecar\sidecar_server.py"
Require-File "PUBLIC\index.html"
Require-File "PUBLIC\research_state.json"
Require-File "scripts\check_desktop_app.ps1"
Require-File "scripts\validate_schemas.ps1"
Require-File "scripts\validate_skills.ps1"
$results += [pscustomobject]@{ Check = "Repository files"; Status = "ok"; Detail = "Desktop app, sidecar, public state, scripts present" }

if ($RequireTauriBuild) {
  $cargo = Find-CommandPath "cargo"
  if (!$cargo) { throw "Tauri build requested but cargo was not found on PATH." }
  $results += [pscustomobject]@{ Check = "Cargo"; Status = "ok"; Detail = ((& cargo --version) -join " ") }
}

$results | Format-Table -AutoSize
Write-Output "Environment check passed. OS package names and install commands may need adjustment for your OS version."
