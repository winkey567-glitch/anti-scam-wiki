$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
git config core.hooksPath .githooks

Write-Host "Git hooks path set to .githooks"
Write-Host "Before each commit, a build check will run automatically."
Write-Host "After each local commit, the current branch will auto-push to origin."
