# Reparation camera USB - a lancer en administrateur
# Clic droit sur PowerShell -> Executer en tant qu'administrateur
# puis: cd vers le dossier du projet
#       powershell -ExecutionPolicy Bypass -File repair_usb_camera.ps1

Write-Host "=== Reparation Camera USB ===" -ForegroundColor Cyan
Write-Host ""

# 1. Etat actuel
Write-Host "1. Cameras detectees par Windows:" -ForegroundColor Yellow
Get-PnpDevice -Class Camera -ErrorAction SilentlyContinue |
    Format-Table FriendlyName, Status, Problem -AutoSize

Write-Host ""
Write-Host "2. Suppression des entrees fantomes 'USB2.0 Camera'..." -ForegroundColor Yellow

$phantoms = Get-PnpDevice -ErrorAction SilentlyContinue |
    Where-Object { $_.FriendlyName -eq "USB2.0 Camera" -and $_.Status -eq "Unknown" }

if ($phantoms) {
    foreach ($dev in $phantoms) {
        Write-Host "   Suppression: $($dev.InstanceId)"
        try {
            pnputil /remove-device $dev.InstanceId 2>$null
            if ($LASTEXITCODE -ne 0) {
                Disable-PnpDevice -InstanceId $dev.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
            }
        } catch {
            Write-Host "   Echec (besoin droits admin?)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "   Aucune entree fantome trouvee."
}

Write-Host ""
Write-Host "3. Peripheriques USB en erreur:" -ForegroundColor Yellow
Get-PnpDevice -ErrorAction SilentlyContinue |
    Where-Object { $_.Problem -ne 0 -and $_.FriendlyName -like "*USB*" } |
    Format-Table FriendlyName, Status, Problem -AutoSize

Write-Host ""
Write-Host "=== MAINTENANT FAITES CECI ===" -ForegroundColor Green
Write-Host "  1. Debranchez la camera USB"
Write-Host "  2. Redemarrez le PC"
Write-Host "  3. Branchez la camera sur un PORT USB DIFFERENT"
Write-Host "  4. Verifiez que la LED de la camera s'allume"
Write-Host "  5. Lancez: python test_usb_shape.py --live"
Write-Host ""
Write-Host "Si Windows installe le driver, vous verrez:" -ForegroundColor Cyan
Write-Host "  [0] USB2.0 Camera (USB)"
Write-Host "  [1] HP HD Camera (integree - ignoree)"
Write-Host ""

Read-Host "Appuyez sur Entree pour fermer"
