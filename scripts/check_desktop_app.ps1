Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Require-File([string]$Path) {
  if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing required file: $Path" }
}

function Forbid-Path([string]$Path) {
  if (Test-Path -LiteralPath $Path) { throw "Forbidden legacy path still exists: $Path" }
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
Require-File "PUBLIC\research_state.json"
Require-File "config\schemas\research_state.schema.json"
Require-File "config\schemas\intake_packet.schema.json"
$legacyCopilot = "copilot"
Forbid-Path "PUBLIC\$legacyCopilot.html"
Forbid-Path "PUBLIC\$($legacyCopilot)_state.json"
Forbid-Path "PUBLIC\index.html"
Forbid-Path "docs\start-here.html"
Forbid-Path "docs\domain-modes.html"
Forbid-Path "docs\technical-report.html"
Forbid-Path "docs\codex-browser-$legacyCopilot.html"
Forbid-Path ".agents\plugins\plugins\research-os-$legacyCopilot"

Require-Text "apps\research-os-desktop\package.json" "@tauri-apps/cli"
Require-Text "apps\research-os-desktop\package.json" "lucide-react"
Require-Text "apps\research-os-desktop\src\tauriDialog.ts" "plugin:dialog|open"
Require-Text "apps\research-os-desktop\src-tauri\Cargo.toml" "tauri-plugin-dialog"
Require-Text "apps\research-os-desktop\src-tauri\tauri.conf.json" "research-os-core"
Require-Text "apps\research-os-desktop\src-tauri\capabilities\default.json" "dialog:default"
Require-Text "apps\research-os-desktop\src-tauri\src\main.rs" "--seed-root"
Require-Text "apps\research-os-desktop\src-tauri\src\main.rs" "tauri_plugin_dialog"
Require-Text "apps\research-os-desktop\src\App.tsx" "submitIntake"
Require-Text "apps\research-os-desktop\src\App.tsx" "FinalProductModal"
Require-Text "apps\research-os-desktop\src\App.tsx" "api.finalProducts"
Require-Text "apps\research-os-desktop\src\components\ChoicePrompt.tsx" "recommended_option"
Require-Text "apps\research-os-desktop\src\components\ChoicePrompt.tsx" "freeForm"
Require-Text "apps\research-os-sidecar\research_os_sidecar\common.py" "research-os-project-v1"
Require-Text "apps\research-os-sidecar\research_os_sidecar\profile_service.py" "Profile metadata must not store secret"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "approval_handler"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "redact_sensitive"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "codex_unavailable"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "Path escapes project sandbox"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "ALLOWED_ORIGINS"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "PUBLIC"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "research_state.json"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "CONTROL"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "intake_queue"
Require-Text "docs\desktop-app.md" ".rosproj"
Require-Text "PUBLIC\dashboard_data.json" "Desktop App"
Require-Text "docs\doc_map.yaml" "desktop_app"

$desktopTextFiles = @(
  "apps\research-os-desktop\src",
  "apps\research-os-desktop\tests"
)
$mojibakeMarkers = @([char]0x9435, [char]0x93c9, [char]0x9356, [char]0x8930, [char]0xfffd)
foreach ($rootPath in $desktopTextFiles) {
  Get-ChildItem -LiteralPath $rootPath -Recurse -File -Include *.ts,*.tsx,*.css | ForEach-Object {
    $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $_.FullName
    foreach ($marker in $mojibakeMarkers) {
      if ($text.Contains([string]$marker)) {
        throw "Desktop UI text contains mojibake marker U+$([int][char]$marker): $($_.FullName)"
      }
    }
  }
}

Write-Output "Desktop app checks passed."
