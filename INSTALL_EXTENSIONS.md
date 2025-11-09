# Installation Guide - Extensions et Packages

## 📦 Packages Python Requis

### Installation automatique
```bash
pip install -r requirements.txt
```

### Installation manuelle
```bash
pip install sqlalchemy pandas rapidfuzz python-docx openpyxl
```

### Packages inclus:
- **sqlalchemy** - ORM pour bases de données
- **pandas** - Manipulation de données
- **rapidfuzz** - Correspondance de chaînes floue
- **python-docx** - Lecture de fichiers Word (.docx)
- **openpyxl** - Lecture/écriture de fichiers Excel

## 🔌 Extensions VS Code Recommandées

### Installation automatique
1. Ouvrez VS Code dans ce dossier
2. VS Code vous proposera d'installer les extensions recommandées
3. Cliquez sur "Install All"

### Extensions principales:

#### Python
- **Python** (ms-python.python) - Support Python complet
- **Pylance** (ms-python.vscode-pylance) - IntelliSense avancé
- **Black Formatter** (ms-python.black-formatter) - Formatage de code
- **isort** (ms-python.isort) - Organisation des imports
- **Flake8** (ms-python.flake8) - Linting Python
- **mypy** (ms-python.mypy-type-checker) - Vérification de types

#### Utilitaires
- **GitLens** (eamodio.gitlens) - Amélioration de Git
- **Prettier** (esbenp.prettier-vscode) - Formatage de code
- **YAML** (redhat.vscode-yaml) - Support YAML
- **PowerShell** (ms-vscode.powershell) - Support PowerShell

#### Jupyter (optionnel)
- **Jupyter** (ms-toolsai.jupyter) - Notebooks Jupyter
- **Jupyter Keymap** (ms-toolsai.jupyter-keymap)
- **Jupyter Renderers** (ms-toolsai.jupyter-renderers)

## 🚀 Installation Rapide

### Windows PowerShell
```powershell
# Installer les packages Python
python -m pip install -r requirements.txt

# Vérifier l'installation
python -c "import sqlalchemy, pandas, rapidfuzz; print('✓ Tous les packages sont installés')"
```

### Vérification
```bash
python -c "import sqlalchemy; print('SQLAlchemy:', sqlalchemy.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import rapidfuzz; print('RapidFuzz: OK')"
python -c "from docx import Document; print('python-docx: OK')"
```

## ⚠️ Problèmes Courants

### ModuleNotFoundError
Si vous obtenez `ModuleNotFoundError`, installez les packages:
```bash
pip install --user sqlalchemy pandas rapidfuzz python-docx
```

### Extensions VS Code non installées
1. Ouvrez VS Code
2. Appuyez sur `Ctrl+Shift+X` (ou `Cmd+Shift+X` sur Mac)
3. Recherchez et installez les extensions listées ci-dessus

### Python non trouvé
Assurez-vous que Python est dans votre PATH:
```bash
python --version
```

## 📝 Notes

- Les extensions VS Code sont optionnelles mais recommandées
- Les packages Python sont **requis** pour exécuter les scripts
- Utilisez un environnement virtuel pour isoler les dépendances:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate  # Windows
  pip install -r requirements.txt
  ```

