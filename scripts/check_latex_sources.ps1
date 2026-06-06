param(
  [string]$PaperDir = "PUBLIC\paper"
)

$ErrorActionPreference = "Stop"

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
