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
Require-File "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx"
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
Require-Text "apps\research-os-desktop\src\App.tsx" "PaperWorkflowPanel"
Require-Text "apps\research-os-desktop\src\components\ChoicePrompt.tsx" "recommended_option"
Require-Text "apps\research-os-desktop\src\components\ChoicePrompt.tsx" "freeForm"
Require-Text "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx" "source_verification"
Require-Text "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx" "recordWorkflowGap"
Require-Text "apps\research-os-sidecar\research_os_sidecar\common.py" "research-os-project-v1"
Require-Text "apps\research-os-sidecar\research_os_sidecar\profile_service.py" "Profile metadata must not store secret"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "approval_handler"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "redact_sensitive"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "codex_unavailable"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "verify venue rules"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "Path escapes project sandbox"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "ALLOWED_ORIGINS"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "/api/workflow-gap"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "/api/paper-artifacts/write"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "/api/import-directory"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "port is already in use"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "import_directory_to_project"
Require-Text "apps\research-os-sidecar\research_os_sidecar\paper_artifact_service.py" "PUBLIC/paper/"
Require-Text "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx" "artifact_status"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "PUBLIC"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "research_state.json"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "CONTROL"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "intake_queue"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "submission_workflow"
Require-Text "docs\desktop-app.md" ".rosproj"
Require-Text "PUBLIC\dashboard_data.json" "Desktop App"
Require-Text "docs\doc_map.yaml" "desktop_app"

$desktopTextFiles = @(
  "apps\research-os-desktop\src",
  "apps\research-os-desktop\tests"
)

$mojibakeCodePoints = @(
  0x9435, 0x93c9, 0x9356, 0x8930, 0xfffd,
  0x942e, 0x95c3, 0x7487, 0x93ba, 0x9352, 0x7039,
  0x20ac, 0x00c3, 0x00c2, 0x9205, 0x9241
)

foreach ($rootPath in $desktopTextFiles) {
  Get-ChildItem -LiteralPath $rootPath -Recurse -File -Include *.ts,*.tsx,*.css | ForEach-Object {
    $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $_.FullName
    foreach ($codePoint in $mojibakeCodePoints) {
      $marker = [char]$codePoint
      if ($text.Contains([string]$marker)) {
        throw "Desktop UI text contains mojibake marker U+$('{0:X4}' -f $codePoint): $($_.FullName)"
      }
    }
  }
}

Write-Output "Desktop app checks passed."
