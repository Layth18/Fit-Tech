# Script PowerShell pour installer tous les packages Python
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation des packages Python" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier Python
try {
    $pythonVersion = python --version
    Write-Host "✓ Python trouvé: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERREUR: Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Mise à jour de pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "Installation des packages depuis requirements.txt..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Vérification de l'installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier les packages
$packages = @(
    @{Name="SQLAlchemy"; Module="sqlalchemy"},
    @{Name="Pandas"; Module="pandas"},
    @{Name="RapidFuzz"; Module="rapidfuzz"},
    @{Name="python-docx"; Module="docx"}
)

foreach ($pkg in $packages) {
    try {
        $version = python -c "import $($pkg.Module); print($($pkg.Module).__version__)" 2>$null
        if ($version) {
            Write-Host "✓ $($pkg.Name): $version" -ForegroundColor Green
        } else {
            Write-Host "✓ $($pkg.Name): OK" -ForegroundColor Green
        }
    } catch {
        Write-Host "✗ $($pkg.Name): Non installé" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation terminée!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pour installer les extensions VS Code:" -ForegroundColor Yellow
Write-Host "1. Ouvrez VS Code dans ce dossier" -ForegroundColor White
Write-Host "2. VS Code proposera d'installer les extensions" -ForegroundColor White
Write-Host "3. Cliquez sur 'Install All'" -ForegroundColor White
Write-Host ""

