param(
  [string]$Message = ""
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($Message)) {
  $Message = "chore: update site $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

Write-Host "Running build check..."
npm run check
if ($LASTEXITCODE -ne 0) {
  throw "Build check failed."
}

Write-Host "Staging changes..."
git add -A
if ($LASTEXITCODE -ne 0) {
  throw "git add failed."
}

$status = git status --short
if ([string]::IsNullOrWhiteSpace(($status | Out-String).Trim())) {
  Write-Host "No changes to commit."
  exit 0
}

Write-Host "Creating commit..."
git commit -m $Message
if ($LASTEXITCODE -ne 0) {
  throw "git commit failed."
}

Write-Host "Done. Post-commit hook will push the current branch to GitHub automatically."
