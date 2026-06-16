param(
  [string]$Root = ".",
  [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"

function Resolve-Python([string]$Requested) {
  $candidates = @()
  if ($Requested) { $candidates += $Requested }
  if ($env:RESEARCH_OS_PYTHON) { $candidates += $env:RESEARCH_OS_PYTHON }
  if ($env:CODEX_PYTHON_PATH) { $candidates += $env:CODEX_PYTHON_PATH }
  if ($env:USERPROFILE) {
    $candidates += (Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe")
  }
  $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
  if ($pythonCmd) { $candidates += $pythonCmd.Source }
  $python3Cmd = Get-Command python3 -ErrorAction SilentlyContinue
  if ($python3Cmd) { $candidates += $python3Cmd.Source }

  foreach ($candidate in $candidates) {
    if (!$candidate) { continue }
    try {
      if ((Test-Path -LiteralPath $candidate) -or (Get-Command $candidate -ErrorAction SilentlyContinue)) {
        & $candidate --version *> $null
        if ($LASTEXITCODE -eq 0) { return $candidate }
      }
    } catch {
      continue
    }
  }
  throw "No usable Python runtime found. Set RESEARCH_OS_PYTHON or CODEX_PYTHON_PATH."
}

$pythonExe = Resolve-Python $PythonPath
& $pythonExe (Join-Path $Root "tools\build_public_summaries.py") --root $Root --check
if ($LASTEXITCODE -ne 0) {
  throw "Public summary check failed."
}
