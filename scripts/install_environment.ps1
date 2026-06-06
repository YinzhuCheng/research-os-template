param(
  [switch]$InstallMissing,
  [switch]$RunValidation,
  [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"

function Has-Command([string]$Name) {
  return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Install-WindowsPackage([string]$Id, [string]$Name) {
  if (!$InstallMissing) {
    Write-Output "Missing ${Name}. Rerun with -InstallMissing or install it manually."
    return
  }
  if (!(Has-Command "winget")) {
    Write-Output "winget is unavailable. Install ${Name} manually or adapt this script for Chocolatey/Scoop/enterprise package management."
    return
  }
  Write-Output "Installing ${Name} with winget. Package IDs can change with OS version; adjust if this fails."
  winget install --id $Id --exact --silent --accept-package-agreements --accept-source-agreements
}

function Get-PowerShellHostCommand() {
  $current = (Get-Process -Id $PID).Path
  if ($current -and (Test-Path -LiteralPath $current)) { return $current }
  $pwsh = Get-Command "pwsh" -ErrorAction SilentlyContinue
  if ($pwsh) { return $pwsh.Source }
  $powershell = Get-Command "powershell" -ErrorAction SilentlyContinue
  if ($powershell) { return $powershell.Source }
  throw "Unable to locate a PowerShell executable for nested validation."
}

$psHost = Get-PowerShellHostCommand

Write-Output "Research OS environment installer"
Write-Output "Note: OS package names and package managers vary by Windows/macOS/Linux version. Adjust commands if needed."

if ($IsMacOS -or $IsLinux) {
  Write-Output "Non-Windows host detected. This script will check the environment, but automatic installs are Windows/winget-oriented."
  Write-Output "Suggested packages: git, python3, powershell 7+. Use brew, apt, dnf, pacman, or your system package manager as appropriate."
}

if (!(Has-Command "git")) {
  Install-WindowsPackage -Id "Git.Git" -Name "Git"
} else {
  Write-Output "Git found: $((git --version) -join ' ')"
}

$pythonCandidate = $PythonPath
if (!$pythonCandidate) {
  if (Has-Command "python") { $pythonCandidate = "python" }
  elseif (Has-Command "python3") { $pythonCandidate = "python3" }
}

if (!$pythonCandidate) {
  Install-WindowsPackage -Id "Python.Python.3.12" -Name "Python 3.12"
} else {
  Write-Output "Python found: $((& $pythonCandidate --version 2>&1) -join ' ')"
}

Write-Output "Checking repository environment..."
if ($PythonPath) {
  & $psHost -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1 -PythonPath $PythonPath -RequireCodexPluginFiles
} else {
  & $psHost -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1 -RequireCodexPluginFiles
}

if ($RunValidation) {
  Write-Output "Running standard validation checks..."
  & $psHost -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_schemas.ps1
  & $psHost -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate_skills.ps1
  & $psHost -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_copilot_bridge.ps1
  & $psHost -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_dashboard.ps1
  & $psHost -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_html_docs.ps1
  & $psHost -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_docs_links.ps1
}

Write-Output ""
Write-Output "Environment is ready for normal local use."
Write-Output "Start the browser copilot bridge with:"
Write-Output "python .agents/plugins/plugins/research-os-copilot/scripts/research_os_copilot_server.py --serve"
Write-Output ""
Write-Output "Then open http://127.0.0.1:8765/ in a browser or Codex in-app Browser."
