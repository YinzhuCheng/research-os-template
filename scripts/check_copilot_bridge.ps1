param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Require-File([string]$Path) {
  $full = Join-Path $Root $Path
  if (!(Test-Path -LiteralPath $full)) { throw "Missing copilot bridge file: $Path" }
}

function Require-Text([string]$Path, [string]$Pattern) {
  $full = Join-Path $Root $Path
  Require-File $Path
  $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $full
  if ($text -notmatch $Pattern) { throw "Copilot bridge check failed: $Path missing $Pattern" }
}

$pluginRoot = ".agents\plugins\plugins\research-os-copilot"
Require-File ".agents\plugins\marketplace.json"
Require-File "$pluginRoot\.codex-plugin\plugin.json"
Require-File "$pluginRoot\.mcp.json"
Require-File "$pluginRoot\skills\research-os-copilot\SKILL.md"
Require-File "$pluginRoot\scripts\research_os_copilot_server.py"
Require-File "skills\research-os-copilot\SKILL.md"
Require-File "scripts\download_reference_links.ps1"
Require-File "PUBLIC\copilot.html"

Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root ".agents\plugins\marketplace.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "$pluginRoot\.codex-plugin\plugin.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $Root "$pluginRoot\.mcp.json") | ConvertFrom-Json | Out-Null

Require-Text ".agents\plugins\marketplace.json" "research-os-copilot"
Require-Text "$pluginRoot\.codex-plugin\plugin.json" "mcpServers"
Require-Text "$pluginRoot\.mcp.json" "research-os-copilot"
Require-Text "$pluginRoot\scripts\research_os_copilot_server.py" "pending_intake_analysis"
Require-Text "$pluginRoot\scripts\research_os_copilot_server.py" "PRIVATE"
Require-Text "skills\research-os-copilot\SKILL.md" "material-first"
Require-Text "skills\research-os-orchestrator\references\routing.md" "research-os-copilot"

Write-Output "Copilot bridge validation passed."
