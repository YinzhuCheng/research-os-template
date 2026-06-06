param(
  [string]$Root = ".",
  [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"

function Require-File([string]$Path) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) {
    throw "Missing harness file: $Path"
  }
}

function Require-Text([string]$Path, [string]$Pattern) {
  $full = Join-Path $Root $Path
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $full
  if ($text -notmatch $Pattern) {
    throw "Harness check failed: $Path missing $Pattern"
  }
}

$required = @(
  "AGENTS.md",
  ".agents\skills",
  ".codex\config.toml.example",
  ".codex\requirements.md",
  ".codex\hooks\pre_tool_use_policy.py",
  ".codex\hooks\post_tool_use_review.py",
  ".codex\hooks\stop_review.py",
  "CONTROL\work_order.yaml",
  "CONTROL\phase_gate.yaml",
  "docs\technical-report.html",
  "docs\start-here.html",
  "docs\integrations\components.yaml",
  "config\schemas\harness_run.schema.json",
  "config\schemas\integration_component.schema.json",
  "config\schemas\doc_map.schema.json",
  "PROVENANCE\run_manifest.jsonl",
  "PROVENANCE\resource_ledger.jsonl",
  "PRIVATE\secrets\README.md"
)

foreach ($path in $required) { Require-File $path }

Require-Text "AGENTS.md" "API key"
Require-Text "AGENTS.md" "feasibility_probe"
Require-Text ".codex\config.toml.example" "PreToolUse"
Require-Text ".codex\config.toml.example" "PostToolUse"
Require-Text ".codex\config.toml.example" "sandbox_mode"
Require-Text "PRIVATE\secrets\README.md" "DO_NOT_STORE_REAL_SECRETS"

$pythonExe = $null
if ($PythonPath -and (Test-Path -LiteralPath $PythonPath)) {
  $pythonExe = $PythonPath
}

$candidateCommands = @()
if ($pythonExe) { $candidateCommands += $pythonExe }
if ($env:RESEARCH_OS_PYTHON -and (Test-Path -LiteralPath $env:RESEARCH_OS_PYTHON)) { $candidateCommands += $env:RESEARCH_OS_PYTHON }
if ($env:CODEX_PYTHON_PATH -and (Test-Path -LiteralPath $env:CODEX_PYTHON_PATH)) { $candidateCommands += $env:CODEX_PYTHON_PATH }
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) { $candidateCommands += "python" }
$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($pyLauncher) { $candidateCommands += "py -3" }

$pythonUsable = $false
foreach ($candidate in $candidateCommands) {
  if ($pythonUsable) { break }
  try {
    if ($candidate -eq "py -3") {
      & py -3 --version *> $null
      if ($LASTEXITCODE -eq 0) {
        $pythonExe = "py -3"
        $pythonUsable = $true
      }
    } else {
      & $candidate --version *> $null
      if ($LASTEXITCODE -eq 0) {
        $pythonExe = $candidate
        $pythonUsable = $true
      }
    }
  } catch {
    $pythonUsable = $false
  }
}

if ($pythonUsable) {
  if ($pythonExe -eq "py -3") {
    & py -3 -m py_compile `
      (Join-Path $Root ".codex\hooks\pre_tool_use_policy.py") `
      (Join-Path $Root ".codex\hooks\post_tool_use_review.py") `
      (Join-Path $Root ".codex\hooks\stop_review.py")
  } else {
    & $pythonExe -m py_compile `
      (Join-Path $Root ".codex\hooks\pre_tool_use_policy.py") `
      (Join-Path $Root ".codex\hooks\post_tool_use_review.py") `
      (Join-Path $Root ".codex\hooks\stop_review.py")
  }
  if ($LASTEXITCODE -ne 0) { throw "Hook Python compile failed." }

  if ($pythonExe -eq "py -3") {
    $blocked = '{"tool":"shell_command","command":"git push origin main"}' | & py -3 (Join-Path $Root ".codex\hooks\pre_tool_use_policy.py") 2>&1
  } else {
    $blocked = '{"tool":"shell_command","command":"git push origin main"}' | & $pythonExe (Join-Path $Root ".codex\hooks\pre_tool_use_policy.py") 2>&1
  }
  if ($LASTEXITCODE -eq 0) {
    throw "PreToolUse hook did not block an external writeback sample."
  }
} else {
  Write-Output "Python runtime not usable; skipped hook py_compile smoke test."
}

Write-Output "Harness check passed."
