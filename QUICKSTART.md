# Quick Start Guide

## Installation

1. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

**Note**: If you don't have TensorFlow or scikit-learn installed, the system will use simplified fallback models. For best results, install all dependencies.

## Basic Usage

### 1. Run the Main Pipeline

```bash
python cycle_to_peak_predictor.py
```

This will:
- Load all data files
- Process the first available player
- Train a prediction model
- Generate a performance prediction
- Display results

### 2. Run Example Scripts

```bash
python example_usage.py
```

This demonstrates:
- Single player analysis
- Team-wide readiness overview
- Visualization generation

### 3. Use in Your Code

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

# Initialize
predictor = CycleToPeakPredictor()

# Load data
predictor.load_all_data()

# Predict for a player
player_data = predictor.prepare_player_data("Player Name", position="midfielder")
predictor.train_model("Player Name")
prediction = predictor.predict_next_match("Player Name")

print(f"Match Readiness: {prediction['match_readiness_score']}/10")
```

## Data Files Required

Place these files in the project directory:
- `training_gps.csv` - GPS training data
- `matchs_gps.csv` - GPS match data (optional)
- `wyscout_matchs.csv` - Match statistics
- `wyscout_players_outfield.csv` - Player match statistics

## Output

The system generates:
1. **Predictions**: Match Readiness Scores (1-10)
2. **Visualizations**: Performance charts (saved as PNG files)
3. **Reports**: Summary dataframes with historical performance

## Troubleshooting

**"No GPS data found"**
- Check that player names match exactly between files
- Ensure `training_gps.csv` contains the player's data

**"Insufficient data"**
- Need at least 15 days of training data
- System will use available data and pad if needed

**Missing dependencies**
- System works with basic Python + pandas/numpy
- Install scikit-learn and TensorFlow for full functionality

## Next Steps

1. Review the `README.md` for detailed documentation
2. Check `example_usage.py` for code examples
3. Customize model parameters in `lstm_predictor.py`
4. Adjust feature selection in `feature_engineering.py`


