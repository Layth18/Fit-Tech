@echo off
echo ========================================
echo Installation des packages Python
echo ========================================
echo.

python --version
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

echo.
echo Installation des packages depuis requirements.txt...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ========================================
echo Verification de l'installation
echo ========================================
python -c "import sqlalchemy; print('✓ SQLAlchemy:', sqlalchemy.__version__)"
python -c "import pandas; print('✓ Pandas:', pandas.__version__)"
python -c "import rapidfuzz; print('✓ RapidFuzz: OK')"
python -c "from docx import Document; print('✓ python-docx: OK')" 2>nul || echo "⚠ python-docx: Non installe (optionnel)"

echo.
echo ========================================
echo Installation terminee!
echo ========================================
echo.
echo Pour installer les extensions VS Code:
echo 1. Ouvrez VS Code dans ce dossier
echo 2. VS Code proposera d'installer les extensions
echo 3. Cliquez sur "Install All"
echo.
pause

