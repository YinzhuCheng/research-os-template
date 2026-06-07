param(
  [string]$ReferenceJson = "PUBLIC\research_state.json",
  [string]$OutputDir = "PRIVATE\references",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $ReferenceJson)) {
  throw "Reference JSON not found: $ReferenceJson"
}

function Get-SafeFileName([string]$Name) {
  $safe = $Name -replace '[\\/:*?"<>|]', '_'
  $safe = $safe.Trim()
  if (!$safe) { $safe = "reference" }
  if ($safe.Length -gt 120) { $safe = $safe.Substring(0, 120) }
  return $safe
}

function Get-DownloadUrl([object]$Ref) {
  $url = [string]$Ref.url
  $policy = [string]$Ref.download_policy
  if ($policy -eq "human_download_required") { return $null }
  if ($url -match "^https://arxiv.org/abs/([0-9]{4}\.[0-9]{4,5}(v[0-9]+)?)") {
    return "https://arxiv.org/pdf/$($Matches[1]).pdf"
  }
  if ($url -match "^https://arxiv.org/pdf/") { return $url }
  if ($policy -eq "landing_page_only") { return $url }
  if ($url -match "^https://") { return $url }
  return $null
}

$payload = Get-Content -Raw -Encoding UTF8 -LiteralPath $ReferenceJson | ConvertFrom-Json
$refs = @()
if ($payload.reference_links) {
  $refs = @($payload.reference_links)
} elseif ($payload.literature -and $payload.literature.reference_links) {
  $refs = @($payload.literature.reference_links)
} else {
  throw "No reference_links found in $ReferenceJson"
}

if (!$DryRun) {
  New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
}

$report = @()
foreach ($ref in $refs) {
  $downloadUrl = Get-DownloadUrl $ref
  $title = if ($ref.title) { [string]$ref.title } else { "reference" }
  $safe = Get-SafeFileName $title
  $policy = [string]$ref.download_policy
  $status = "skipped"
  $outputPath = $null
  $message = ""

  if (!$downloadUrl) {
    $message = "Skipped by policy or unsupported URL. Human download may be required."
  } elseif ($DryRun) {
    $status = "dry_run"
    $message = "Would attempt $downloadUrl"
  } else {
    $extension = if ($downloadUrl -match "\.pdf($|\?)") { ".pdf" } else { ".html" }
    $outputPath = Join-Path $OutputDir "$safe$extension"
    try {
      Invoke-WebRequest -Uri $downloadUrl -OutFile $outputPath -MaximumRedirection 5 -UseBasicParsing
      $status = "downloaded"
      $message = "Downloaded from open URL or landing page."
    } catch {
      $status = "failed"
      $message = $_.Exception.Message
      $outputPath = $null
    }
  }

  $report += [ordered]@{
    title = $title
    url = [string]$ref.url
    attempted_url = $downloadUrl
    policy = $policy
    status = $status
    output_path = $outputPath
    message = $message
  }
}

if (!$DryRun) {
  $reportPath = Join-Path $OutputDir "download_report.json"
  $report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $reportPath -Encoding UTF8
  Write-Output "Reference download report: $reportPath"
} else {
  $report | ConvertTo-Json -Depth 6
}
