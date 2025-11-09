# Export Instructions for Main Project

## 📦 Folder to Export

**Export the entire `ai_module_export` folder** to your main project.

## ✅ Files to Include (Essential)

### Core Python Modules (7 files):
1. ✅ `cycle_to_peak_predictor.py` - Main AI pipeline
2. ✅ `data_loader.py` - Data loading and preprocessing
3. ✅ `training_cycle.py` - Training cycle calculation
4. ✅ `feature_engineering.py` - Feature extraction
5. ✅ `performance_rating.py` - Performance rating system
6. ✅ `lstm_predictor.py` - LSTM prediction model
7. ✅ `visualization.py` - Visualization functions

### Configuration & Documentation (4 files):
8. ✅ `requirements.txt` - Python dependencies
9. ✅ `README.md` - Main documentation
10. ✅ `QUICKSTART.md` - Quick start guide
11. ✅ `example_usage.py` - Usage examples

### Data Files (Optional - only if needed):
12. ⚠️ `training_gps.csv` - GPS training data (if your main project needs sample data)
13. ⚠️ `matchs_gps.csv` - GPS match data (if your main project needs sample data)
14. ⚠️ `wyscout_matchs.csv` - Match statistics (if your main project needs sample data)
15. ⚠️ `wyscout_players_outfield.csv` - Player statistics (if your main project needs sample data)

## ❌ Files to EXCLUDE (Do NOT export):

1. ❌ `__pycache__/` - Python cache folder (auto-generated)
2. ❌ `*.png` - Generated visualization files (e.g., `training_cycle.png`, `team_readiness_dashboard.png`)
   - These are output files, not source code

## 📋 Quick Export Checklist

### Option 1: Export Everything (Recommended for first time)
```
Copy the entire ai_module_export folder, then delete:
- __pycache__ folder
- *.png files
```

### Option 2: Export Only Source Code
```
Copy only these files:
- All .py files (7 files)
- requirements.txt
- README.md
- QUICKSTART.md
- example_usage.py
```

## 🎯 Integration Steps

1. **Copy the folder** to your main project directory
2. **Rename if needed** (e.g., `ai_module`, `performance_predictor`, etc.)
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Import in your main project**:
   ```python
   from ai_module_export.cycle_to_peak_predictor import CycleToPeakPredictor
   # or if you renamed the folder:
   from ai_module.cycle_to_peak_predictor import CycleToPeakPredictor
   ```

## 📁 Recommended Folder Structure in Main Project

```
main_project/
├── ai_module/              # (or whatever you name it)
│   ├── cycle_to_peak_predictor.py
│   ├── data_loader.py
│   ├── training_cycle.py
│   ├── feature_engineering.py
│   ├── performance_rating.py
│   ├── lstm_predictor.py
│   ├── visualization.py
│   ├── example_usage.py
│   ├── requirements.txt
│   ├── README.md
│   └── QUICKSTART.md
├── data/                   # Your actual data files
│   ├── training_gps.csv
│   ├── wyscout_matchs.csv
│   └── ...
└── main.py                 # Your main application
```

## ✅ Verification

After exporting, verify the module works:
```bash
cd ai_module_export  # (or your renamed folder)
python cycle_to_peak_predictor.py
```

If it runs without errors, the export was successful!

