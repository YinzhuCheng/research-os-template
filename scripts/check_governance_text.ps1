param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Read-Text([string]$Path) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Missing governance file: $Path" }
  Get-Content -Raw -Encoding UTF8 -LiteralPath $full
}

function Require-Text([string]$Path, [string]$Needle) {
  $text = Read-Text $Path
  if ($text -notlike "*$Needle*") { throw "Missing '$Needle' in $Path" }
}

$files = @(
  "AGENTS.md",
  ".codex\requirements.md",
  "CONTROL\README.md",
  "skills\README.md",
  "docs\process-contract.md"
)

$mojibakePatterns = @(
  @{ Name = "unicode replacement character"; Regex = "\uFFFD" },
  @{ Name = "latin mojibake marker"; Regex = "[\u00C2\u00C3\u00E2]" },
  @{ Name = "common CJK mojibake marker"; Regex = "[\u951F\u8119\u8117\u95B8\u95B5\u6D94\u9414\u7F01\u9356\u9286\u4E63]" }
)

foreach ($file in $files) {
  $text = Read-Text $file
  foreach ($pattern in $mojibakePatterns) {
    if ($text -match $pattern.Regex) {
      throw "Potential unreadable mojibake marker '$($pattern.Name)' found in $file"
    }
  }
}

Require-Text "AGENTS.md" "Priority Order"
Require-Text "AGENTS.md" "Use Repo Skills First"
Require-Text "AGENTS.md" "config/research_flow.yaml"
Require-Text "AGENTS.md" "work_order.yaml"
Require-Text "AGENTS.md" "phase_gate.yaml"
Require-Text "AGENTS.md" "research-os-orchestrator"
Require-Text "AGENTS.md" "research-os-research-kernel"
Require-Text "AGENTS.md" "research-os-execution-harness"
Require-Text "AGENTS.md" "PRIVATE/"
Require-Text ".codex\requirements.md" "Skill Discovery"
Require-Text ".codex\requirements.md" ".agents/skills/"
Require-Text ".codex\requirements.md" "config/research_flow.yaml"
Require-Text "CONTROL\README.md" "control plane"
Require-Text "CONTROL\README.md" "config/research_flow.yaml"
Require-Text "skills\README.md" "Main Trigger Matrix"
Require-Text "skills\README.md" "Boundary"
Require-Text "docs\process-contract.md" "Canonical Flow"
Require-Text "docs\process-contract.md" "Anti-Spaghetti Rules"

Write-Output "Governance text readability check passed."
