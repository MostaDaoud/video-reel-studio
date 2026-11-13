# install.ps1 — install video-reel-studio for OpenCode on Windows
#   powershell -ExecutionPolicy Bypass -File install.ps1
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Global
param([switch]$Global)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$src  = Join-Path $here "skill\video-reel-studio"

if ($Global) { $dest = Join-Path $HOME ".config\opencode\skills" }
else         { $dest = Join-Path (Get-Location) ".opencode\skills" }

Write-Host "-> installing into $dest"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$target = Join-Path $dest "video-reel-studio"
if (Test-Path $target) { Remove-Item $target -Recurse -Force }
Copy-Item $src $target -Recurse
Write-Host "  OK video-reel-studio"

$missing = @()
foreach ($s in @("video-ad-editor","montage-video","motion-video","podcast-video","thumbnail-video","review-video")) {
  if ((Test-Path (Join-Path $dest $s)) -or (Test-Path (Join-Path $HOME ".config\opencode\skills\$s"))) {
    Write-Host "  OK $s"
  } else {
    Write-Host "  MISSING $s"
    $missing += $s
  }
}

if ($missing.Count -gt 0) {
  Write-Host ""
  Write-Host "Install the production skills first:"
  Write-Host "  git clone https://github.com/majedphotos/video-ad-editor $env:TEMP\vae"
  Write-Host "  Copy-Item $env:TEMP\vae\video-ad-editor,$env:TEMP\vae\montage-video,$env:TEMP\vae\motion-video,$env:TEMP\vae\podcast-video,$env:TEMP\vae\thumbnail-video,$env:TEMP\vae\review-video `"$dest`" -Recurse"
}

Write-Host ""
Write-Host "-> environment check"
python (Join-Path $target "scripts\preflight.py")

Write-Host ""
Write-Host "Done. Open OpenCode and say: «منتج الفيديو ده»"
