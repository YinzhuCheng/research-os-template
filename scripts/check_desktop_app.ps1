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
Require-Text "apps\research-os-desktop\src\App.tsx" "MaterialManifestCard"
Require-Text "apps\research-os-desktop\src\App.tsx" "Research plan generated"
Require-Text "apps\research-os-desktop\src\App.tsx" "The plan has been accepted"
Require-Text "apps\research-os-desktop\src\App.tsx" "Imported sources"
Require-Text "apps\research-os-desktop\src\App.tsx" "importDirectory"
Require-Text "apps\research-os-desktop\src\tauriDialog.ts" "selectMaterialDirectory"
Require-Text "apps\research-os-desktop\src\App.tsx" "FinalProductModal"
Require-Text "apps\research-os-desktop\src\App.tsx" "api.finalProducts"
Require-Text "apps\research-os-desktop\src\App.tsx" "PaperWorkflowPanel"
Require-Text "apps\research-os-desktop\src\components\ChoicePrompt.tsx" "recommended_option"
Require-Text "apps\research-os-desktop\src\components\ChoicePrompt.tsx" "freeForm"
Require-Text "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx" "source_verification"
Require-Text "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx" "research_loop_artifacts"
Require-Text "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx" "Claim-Evidence Matrix"
Require-Text "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx" "recordWorkflowGap"
Require-Text "apps\research-os-sidecar\research_os_sidecar\common.py" "research-os-project-v1"
Require-Text "apps\research-os-sidecar\research_os_sidecar\profile_service.py" "Profile metadata must not store secret"
Require-Text "apps\research-os-sidecar\research_os_sidecar\project_service.py" "project_context.md"
Require-Text "apps\research-os-sidecar\research_os_sidecar\project_service.py" "whole-folder material manifest"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "approval_handler"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "redact_sensitive"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "codex_unavailable"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "verify venue rules"
Require-Text "apps\research-os-sidecar\research_os_sidecar\runtime_service.py" "CONTROL/project_context.md"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "Path escapes project sandbox"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "ALLOWED_ORIGINS"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "/api/workflow-gap"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "/api/research-plan/write"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "/api/research-loop-artifacts/write"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "/api/paper-artifacts/write"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "/api/import-directory"
Require-Text "apps\research-os-sidecar\research_os_sidecar\server.py" "port is already in use"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "import_directory_to_project"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "research-material-manifest-v1"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "_write_public_manifest_summary"
Require-Text "apps\research-os-sidecar\research_os_sidecar\security.py" "classify_material_role"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "material_manifest"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "write_research_plan"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "Do you accept the current research plan"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "CP-FIRST-RESEARCH-LOOP"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "CP-RESEARCH-LOOP-ARTIFACT-ACCEPTANCE"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "repair_blocking_gaps"
Require-Text "apps\research-os-sidecar\research_os_sidecar\research_loop_artifact_service.py" "PUBLIC/research_loop/"
Require-Text "apps\research-os-sidecar\research_os_sidecar\research_loop_artifact_service.py" "research_loop_artifacts_ready_for_acceptance"
Require-Text "apps\research-os-sidecar\research_os_sidecar\archive_service.py" ".research-os"
Require-Text "apps\research-os-desktop\src\api.ts" "writeResearchPlan"
Require-Text "apps\research-os-desktop\src\api.ts" "writeResearchLoopArtifacts"
Require-Text "apps\research-os-sidecar\research_os_sidecar\paper_artifact_service.py" "PUBLIC/paper/"
Require-Text "apps\research-os-desktop\src\components\PaperWorkflowPanel.tsx" "artifact_status"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "PUBLIC"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "research_state.json"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "CONTROL"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "intake_queue"
Require-Text "apps\research-os-sidecar\research_os_sidecar\state_service.py" "submission_workflow"
Require-Text "apps\research-os-sidecar\research_os_sidecar\project_service.py" "Structured Research Plan"
Require-Text "docs\desktop-app.md" ".rosproj"
Require-Text "PUBLIC\dashboard_data.json" "Desktop App"
Require-Text "docs\doc_map.yaml" "desktop_app"

$desktopTextRoots = @(
  "apps\research-os-desktop\src",
  "apps\research-os-desktop\tests"
)

$mojibakeCodePoints = @(
  0x9435, 0x93c9, 0x9356, 0x8930, 0xfffd,
  0x942e, 0x95c3, 0x7487, 0x93ba, 0x9352, 0x7039,
  0x20ac, 0x00c3, 0x00c2, 0x9205, 0x9241
)

$mojibakeAsciiRegexes = @(
  "\?/(strong|p|span|small|button|section|summary|details|label)",
  "\?[A-Za-z]*(rofile|oken)"
)

foreach ($rootPath in $desktopTextRoots) {
  Get-ChildItem -LiteralPath $rootPath -Recurse -File -Include *.ts,*.tsx,*.css | ForEach-Object {
    $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $_.FullName
    foreach ($codePoint in $mojibakeCodePoints) {
      $marker = [char]$codePoint
      if ($text.Contains([string]$marker)) {
        throw "Desktop UI text contains mojibake marker U+$('{0:X4}' -f $codePoint): $($_.FullName)"
      }
    }
    foreach ($regex in $mojibakeAsciiRegexes) {
      if ($text -match $regex) {
        throw "Desktop UI text contains mojibake-like ASCII fallback matching '$regex': $($_.FullName)"
      }
    }
    foreach ($char in $text.ToCharArray()) {
      $codePoint = [int][char]$char
      if (($codePoint -ge 0x4E00 -and $codePoint -le 0x9FFF) -or ($codePoint -ge 0x3400 -and $codePoint -le 0x4DBF)) {
        throw "Desktop UI text contains CJK character U+$('{0:X4}' -f $codePoint) in English-mode workflow: $($_.FullName)"
      }
    }
  }
}

Write-Output "Desktop app checks passed."
