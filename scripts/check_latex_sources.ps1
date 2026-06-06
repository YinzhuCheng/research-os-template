param(
  [string]$PaperDir = "PUBLIC\paper",
  [switch]$Force
)

$ErrorActionPreference = "Stop"

$configPath = "config\research_project.yaml"
if (!$Force -and (Test-Path -LiteralPath $configPath)) {
  $config = Get-Content -Raw -Encoding UTF8 -LiteralPath $configPath
  if ($config -match "paper_enabled:\s*false") {
    Write-Output "LaTeX source static check skipped because dissemination.paper_enabled is false. Use -Force to check paper templates."
    exit 0
  }
}

$required = @(
  "main.tex",
  "appendix.tex",
  "references.bib",
  "figures\method_overview.tikz",
  "figures\result_plot_example.tex",
  "submission_checklist.md"
)

foreach ($file in $required) {
  $path = Join-Path $PaperDir $file
  if (!(Test-Path -LiteralPath $path)) {
    throw "Missing paper file: $path"
  }
}

$main = Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $PaperDir "main.tex")
foreach ($token in @("booktabs", "siunitx", "tikz", "pgfplots", "\appendix")) {
  if ($main -notlike "*$token*") {
    throw "main.tex missing expected token: $token"
  }
}

Write-Output "LaTeX source static check passed."
