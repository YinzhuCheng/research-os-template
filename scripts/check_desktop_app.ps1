Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Require-File([string]$Path) {
  if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing required file: $Path" }
}

function Require-Text([string]$Path, [string]$Needle) {
  Require-File $Path
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $Path
  if ($text -notlike "*$Needle*") { throw "$Path missing required text: $Needle" }
}

Require-File "apps\research-os-desktop\package.json"
Require-File "apps\research-os-desktop\src\App.tsx"
Require-File "apps\research-os-desktop\src\components\ChoicePrompt.tsx"
Require-File "apps\research-os-desktop\src-tauri\tauri.conf.json"
Require-File "apps\research-os-sidecar\sidecar_server.py"
Require-File "apps\research-os-sidecar\research_os_sidecar\server.py"
Require-File "apps\research-os-sidecar\research_os_sidecar\project_service.py"
Require-File "apps\research-os-sidecar\research_os_sidecar\runtime_service.py"
Require-File "apps\research-os-sidecar\tests\test_sidecar_services.py"

Require-Text "apps\research-os-desktop\package.json" "@tauri-apps/cli"
Require-Text "apps\research-os-desktop\package.json" "lucide-react"
Require-Text "apps\research-os-desktop\src\App.tsx" "FinalProductModal"
Require-Text "apps\research-os-desktop\src\App.tsx" "api.finalProducts"
Require-Text "apps\research-os-desktop\src\components\ChoicePrompt.tsx" "recommended_option"
Require-Text "apps\research-os-desktop\src\components\ChoicePrompt.tsx" "free_form"
Require-Text "apps\research-os-sidecar\research_os_sidecar\common.py" "research-os-project-v1"
Require-Text "apps\research-os-sidecar\research_os_sidecar\profile_service.py" "Profile metadata must not store secret"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "approval_handler"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "codex_unavailable"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "Path escapes project sandbox"
Require-Text "docs\desktop-app.md" ".rosproj"
Require-Text "PUBLIC\dashboard_data.json" "Desktop App"
Require-Text "docs\doc_map.yaml" "desktop_app"

Write-Output "Desktop app checks passed."
