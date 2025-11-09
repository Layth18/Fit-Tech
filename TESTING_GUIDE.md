# Testing Guide for AI Module

This guide explains how to test the Cycle-to-Peak Performance Predictor AI module.

## Quick Start

### Option 1: Run the Complete Test Suite (Recommended)

```bash
cd ai_module_export
python test_ai_module.py
```

This will run all tests:
1. **Data Loading Test** - Verifies that CSV files load correctly
2. **Model Components Test** - Tests all module components
3. **Single Player Prediction** - Tests prediction for one player
4. **Multiple Players Test** - Tests predictions for multiple players
5. **Visualization Test** - Generates charts and graphs

### Option 2: Use the Example Script

```bash
python example_usage.py
```

This runs comprehensive examples from the main module.

### Option 3: Run the Main Pipeline

```bash
python cycle_to_peak_predictor.py
```

This runs a simple example with the first available player.

---

## Manual Testing in Python

### Basic Test

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

# Initialize the predictor
predictor = CycleToPeakPredictor()

# Load all data
predictor.load_all_data()

# Get list of available players
players = predictor.data_loader.gps_data['name'].unique()
print(f"Available players: {list(players)}")

# Select a player to test
player_name = players[0]  # Use first player

# Prepare the player's data
player_data = predictor.prepare_player_data(player_name, position='midfielder')

# Train the model
predictor.train_model(player_name)

# Make a prediction
prediction = predictor.predict_next_match(player_name)

# View results
print(f"Player: {prediction['player_name']}")
print(f"Match Readiness Score: {prediction['match_readiness_score']}/10")
print(f"Days Until Match: {prediction['days_until_match']}")
```

### Advanced Test with Validation

```python
from cycle_to_peak_predictor import CycleToPeakPredictor
import pandas as pd

predictor = CycleToPeakPredictor()
predictor.load_all_data()

# Test multiple players
results = []
for player_name in predictor.data_loader.gps_data['name'].unique()[:5]:
    try:
        predictor.prepare_player_data(player_name, position='midfielder')
        predictor.train_model(player_name)
        prediction = predictor.predict_next_match(player_name)
        results.append(prediction)
        print(f"{player_name}: {prediction['match_readiness_score']:.2f}/10")
    except Exception as e:
        print(f"{player_name}: Error - {e}")

# Analyze results
df = pd.DataFrame(results)
print(f"\nAverage Score: {df['match_readiness_score'].mean():.2f}/10")
print(f"Range: {df['match_readiness_score'].min():.2f} - {df['match_readiness_score'].max():.2f}/10")
```

---

## Understanding Test Results

### Match Readiness Score
- **Scale**: 1-10
- **Interpretation**:
  - **7-10**: Player is ready for match (optimal performance expected)
  - **5-7**: Moderate readiness (acceptable performance)
  - **1-5**: Low readiness (risk of poor performance or fatigue)

### Test Outputs

#### Successful Test Output:
```
[OK] GPS data loaded: 7903 records
[OK] Model trained successfully
[OK] Prediction score is valid (1-10 range)
```

#### Failed Test Output:
```
[FAIL] GPS file not found: training_gps.csv
[FAIL] Error in prediction: ...
```

---

## What Each Test Checks

### Test 1: Data Loading
- ✅ Verifies CSV files exist and can be loaded
- ✅ Checks data structure and columns
- ✅ Lists available players

### Test 2: Model Components
- ✅ Verifies all components are initialized
- ✅ Checks TensorFlow availability
- ✅ Validates model configuration

### Test 3: Single Player Prediction
- ✅ Tests data preparation
- ✅ Tests model training
- ✅ Tests prediction generation
- ✅ Validates prediction range (1-10)

### Test 4: Multiple Players
- ✅ Tests batch processing
- ✅ Tests error handling
- ✅ Generates summary statistics

### Test 5: Visualization
- ✅ Tests chart generation
- ✅ Saves test images
- ✅ Verifies visualization functions

---

## Troubleshooting

### Error: "GPS file not found"
**Solution:** Ensure `training_gps.csv` is in the `ai_module_export` folder

### Error: "No players found in dataset"
**Solution:** Check that the CSV file has a `name` column with player names

### Error: "Insufficient data"
**Solution:** Need at least 15 records per player for optimal predictions

### Error: "TensorFlow not available"
**Solution:** This is OK - the module will use a fallback linear regression model
- For full functionality: `pip install tensorflow`
- For ONNX export: TensorFlow is required

### Error: "Model training failed"
**Possible causes:**
- Insufficient data (< 15 records)
- Missing required columns in CSV
- Data format issues

**Solution:** Check data quality and ensure all required columns are present

---

## Expected Test Results

### Successful Test Run:
```
TEST SUMMARY
============================================================
Data Loading: [PASSED]
Model Components: [PASSED]
Single Player: [PASSED]
Multiple Players: [PASSED]
Visualization: [PASSED]

Total: 5/5 tests passed

[SUCCESS] All tests passed! The AI module is working correctly.
```

### Partial Success (with warnings):
```
Data Loading: [PASSED]
Model Components: [PASSED]
Single Player: [PASSED]
Multiple Players: [PASSED]
Visualization: [FAILED]

Total: 4/5 tests passed

[WARNING] 1 test(s) failed. Please review the errors above.
```

---

## Testing Specific Features

### Test ONNX Export (if TensorFlow installed)

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

predictor = CycleToPeakPredictor()
predictor.load_all_data()
predictor.prepare_player_data("Player Name", position="midfielder")
predictor.train_model("Player Name")

# Export to ONNX
lstm_predictor = predictor.lstm_predictor
if lstm_predictor.TENSORFLOW_AVAILABLE and lstm_predictor.is_trained:
    success = lstm_predictor.export_to_onnx("test_model.onnx")
    if success:
        print("[OK] ONNX export successful")
    else:
        print("[FAIL] ONNX export failed")
else:
    print("[WARNING] Cannot export - TensorFlow not available or model not trained")
```

### Test Visualization

```python
from cycle_to_peak_predictor import CycleToPeakPredictor
from visualization import PerformanceVisualizer
import matplotlib.pyplot as plt

predictor = CycleToPeakPredictor()
predictor.load_all_data()
predictor.prepare_player_data("Player Name", position="midfielder")
predictor.train_model("Player Name")
prediction = predictor.predict_next_match("Player Name")

# Generate visualizations
visualizer = PerformanceVisualizer()
evolution = predictor.get_performance_evolution("Player Name")
cycle = predictor.get_training_cycle_summary("Player Name")

if len(evolution) > 0:
    fig = visualizer.plot_performance_evolution(evolution, prediction['predicted_rating'])
    plt.savefig('test_evolution.png')
    print("[OK] Evolution chart saved")

if len(cycle) > 0:
    fig = visualizer.plot_training_cycle(cycle)
    plt.savefig('test_cycle.png')
    print("[OK] Cycle chart saved")
```

---

## Performance Benchmarks

### Expected Performance:
- **Data Loading**: < 5 seconds for typical datasets
- **Model Training**: 10-60 seconds (depends on data size and TensorFlow)
- **Prediction**: < 1 second per player
- **Visualization**: < 2 seconds per chart

### Memory Usage:
- **Typical**: 200-500 MB
- **With TensorFlow**: 500 MB - 2 GB

---

## Next Steps After Testing

1. **If all tests pass**: The module is ready to use!
2. **If some tests fail**: Review error messages and check data quality
3. **For production**: Run tests regularly to ensure module integrity
4. **For deployment**: Export models to ONNX format for deployment

---

## Summary

✅ **Quick Test**: `python test_ai_module.py`  
✅ **Example Usage**: `python example_usage.py`  
✅ **Main Pipeline**: `python cycle_to_peak_predictor.py`  
✅ **Manual Testing**: Use the Python code examples above  

**Your AI module is tested and ready!** 🚀

