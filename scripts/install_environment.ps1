param(
  [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

Write-Output "Research OS Desktop environment"
Write-Output "Required: Git, Python 3.10+, Node/npm for frontend development, Rust/Cargo for Tauri packaging."

if ($CheckOnly) {
  & powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1 -RequireTauriBuild
  exit $LASTEXITCODE
}

Write-Output "This script does not install system packages automatically."
Write-Output "After installing prerequisites, run:"
Write-Output "  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_environment.ps1 -RequireTauriBuild"
Write-Output "  cd apps\research-os-desktop; npm install; npm run tauri -- build"
