param(
  [string[]]$HtmlDocs = @("docs\start-here.html", "docs\domain-modes.html", "docs\technical-report.html", "PUBLIC\index.html")
)

$ErrorActionPreference = "Stop"

foreach ($path in $HtmlDocs) {
  if (!(Test-Path -LiteralPath $path)) {
    throw "HTML document missing: $path"
  }
  $html = Get-Content -Raw -Encoding UTF8 -LiteralPath $path
  foreach ($item in @("<!doctype html>", "<html", "<meta name=""viewport""", "</html>")) {
    if ($html.ToLowerInvariant() -notlike "*$($item.ToLowerInvariant())*") {
      throw "HTML check failed for ${path}: missing $item"
    }
  }
  $lastClose = $html.LastIndexOf("</html>", [System.StringComparison]::OrdinalIgnoreCase)
  if ($lastClose -lt 0) { throw "HTML check failed for ${path}: missing closing html tag." }
  if ($html.Substring($lastClose + 7).Trim().Length -gt 0) {
    throw "HTML check failed for ${path}: non-whitespace content after </html>."
  }
  if ($html -match "(?i)<script\s+[^>]*src\s*=") {
    throw "HTML check failed for ${path}: external script src is not allowed."
  }
  if ($html -match "(?i)<link\s+[^>]*href\s*=\s*['""]https?://") {
    throw "HTML check failed for ${path}: remote stylesheet/font link is not allowed."
  }
  Write-Output "HTML doc OK: $path"
}

Write-Output "HTML documentation check passed."
