# Enable Windows Virtualization Features for Docker Desktop
# Run this script as Administrator

Write-Host "Enabling Windows virtualization features..." -ForegroundColor Cyan

# Enable Virtual Machine Platform
Write-Host "`nEnabling Virtual Machine Platform..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Enable WSL 2
Write-Host "`nEnabling Windows Subsystem for Linux..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Hyper-V
Write-Host "`nEnabling Hyper-V..." -ForegroundColor Yellow
try {
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All -NoRestart -ErrorAction Stop
    Write-Host "Hyper-V enabled successfully!" -ForegroundColor Green
} catch {
    Write-Host "Note: Hyper-V may not be available on this device. Docker can still work with WSL 2 backend." -ForegroundColor Yellow
}

Write-Host "`n" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "VIRTUALIZATION FEATURES ENABLED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nYou MUST restart your computer for changes to take effect." -ForegroundColor Cyan
Write-Host "`nAfter restart:" -ForegroundColor White
Write-Host "  1. Start Docker Desktop" -ForegroundColor White
Write-Host "  2. Wait for green 'Running' status" -ForegroundColor White
Write-Host "  3. Return to continue setup" -ForegroundColor White
Write-Host "`n"

$restart = Read-Host "Restart now? (Y/N)"
if ($restart -eq 'Y' -or $restart -eq 'y') {
    Write-Host "Restarting in 10 seconds..." -ForegroundColor Yellow
    shutdown /r /t 10
} else {
    Write-Host "Please restart manually when ready." -ForegroundColor Yellow
}
