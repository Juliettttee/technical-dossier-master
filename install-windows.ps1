# Technical Dossier Master v2.3 - Windows single-source installer
# Run from the maintained project directory. A directory junction points Codex to this source.
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'technical-dossier-master'
if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) { throw 'SKILL.md not found beside installer.' }
$skillRoot = Join-Path $HOME '.agents\skills'
$backupRoot = Join-Path $HOME '.agents\skill-backups'
$dest = Join-Path $skillRoot 'technical-dossier-master'
New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null

if (Test-Path -LiteralPath $dest) {
  $existing = Get-Item -LiteralPath $dest -Force
  if ($existing.LinkType -eq 'Junction' -and $existing.Target -contains $source) {
    Write-Host ('ALREADY LINKED: ' + $dest + ' -> ' + $source) -ForegroundColor Green
    exit 0
  }
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $backup = Join-Path $backupRoot ('technical-dossier-master-backup-' + $stamp)
  if (Test-Path -LiteralPath $backup) { throw ('Backup path already exists: ' + $backup) }
  Move-Item -LiteralPath $dest -Destination $backup
  Write-Host ('Previous installation preserved at: ' + $backup)
}

try {
  New-Item -ItemType Junction -Path $dest -Target $source | Out-Null
} catch {
  if ($backup -and (Test-Path -LiteralPath $backup) -and -not (Test-Path -LiteralPath $dest)) {
    Move-Item -LiteralPath $backup -Destination $dest
    Write-Warning 'Junction creation failed; the previous installation was restored.'
  }
  throw
}

$installed = Get-Item -LiteralPath $dest -Force
if ($installed.LinkType -ne 'Junction' -or -not (Test-Path -LiteralPath (Join-Path $dest 'SKILL.md'))) {
  throw 'Installation verification failed: destination is not a working junction.'
}
Write-Host ('LINKED: ' + $dest + ' -> ' + $source) -ForegroundColor Green
Write-Host ('Single Resource Packs directory: ' + (Join-Path $source 'resource-packs')) -ForegroundColor Green
if ($backup) { Write-Host ('Backup retained; review it manually before any later removal: ' + $backup) }
$legacy = Join-Path $HOME '.codex\skills\technical-dossier-master\SKILL.md'
if (Test-Path -LiteralPath $legacy) { Write-Warning ('A second copy exists here: ' + $legacy + '. Review for duplicate Skill versions.') }
Write-Host 'Restart Codex after changing SKILL.md. Resource file additions are visible on the next task-start scan without reinstalling.'
