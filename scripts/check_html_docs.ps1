param(
  [string[]]$HtmlDocs = @("docs\start-here.html", "docs\technical-report.html", "PUBLIC\index.html")
)

$ErrorActionPreference = "Stop"

foreach ($path in $HtmlDocs) {
  if (!(Test-Path -LiteralPath $path)) {
    throw "HTML document missing: $path"
  }
  $html = Get-Content -Raw -Encoding UTF8 -LiteralPath $path
  $required = @("<!doctype html>", "<html", "<meta name=""viewport""", "</html>")
  foreach ($item in $required) {
    if ($html.ToLowerInvariant() -notlike "*$($item.ToLowerInvariant())*") {
      throw "HTML check failed for ${path}: missing $item"
    }
  }
  if ($html -match "(?i)<script\s+[^>]*src\s*=") {
    throw "HTML check failed for ${path}: external script src is not allowed."
  }
  if ($html -match "(?i)<link\s+[^>]*href\s*=\s*['""]https?://") {
    throw "HTML check failed for ${path}: remote stylesheet/font link is not allowed."
  }
  if ($path -like "docs\*.html") {
    foreach ($needle in @("README.md", "work_order.yaml", "phase_gate.yaml", "PUBLIC/index.html")) {
      if ($html -notlike "*$needle*") {
        throw "HTML check failed for ${path}: missing repository link $needle"
      }
    }
    if ($html -notlike "*<svg*") {
      throw "HTML check failed for ${path}: expected an inline SVG diagram."
    }
  }
  Write-Output "HTML doc OK: $path"
}

Write-Output "HTML documentation check passed."
