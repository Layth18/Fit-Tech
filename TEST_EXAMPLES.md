# Test Examples - Quick Reference

This file contains ready-to-use code examples for testing the AI model.

## Quick Start

### Run All Examples
```bash
python test_examples.py
```

### Run Individual Examples
```python
from test_examples import example_1_basic_test
example_1_basic_test()
```

---

## Example 1: Basic Single Player Test

**What it does:** Tests prediction for one player

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

predictor = CycleToPeakPredictor()
predictor.load_all_data()

player_name = predictor.data_loader.gps_data['name'].unique()[0]
predictor.prepare_player_data(player_name, position='midfielder')
predictor.train_model(player_name)
prediction = predictor.predict_next_match(player_name)

print(f"Score: {prediction['match_readiness_score']}/10")
```

**Run it:**
```bash
python -c "from test_examples import example_1_basic_test; example_1_basic_test()"
```

---

## Example 2: Multiple Players Test

**What it does:** Tests predictions for multiple players and shows summary

```python
from cycle_to_peak_predictor import CycleToPeakPredictor
import pandas as pd

predictor = CycleToPeakPredictor()
predictor.load_all_data()

players = predictor.data_loader.gps_data['name'].unique()[:5]
results = []

for player_name in players:
    predictor.prepare_player_data(player_name, position='midfielder')
    predictor.train_model(player_name)
    prediction = predictor.predict_next_match(player_name)
    results.append(prediction)
    print(f"{player_name}: {prediction['match_readiness_score']:.2f}/10")

# Summary
df = pd.DataFrame(results)
print(f"Average: {df['match_readiness_score'].mean():.2f}/10")
```

**Run it:**
```bash
python -c "from test_examples import example_2_multiple_players; example_2_multiple_players()"
```

---

## Example 3: Test with Visualization

**What it does:** Generates charts and saves them as PNG files

```python
from cycle_to_peak_predictor import CycleToPeakPredictor
from visualization import PerformanceVisualizer
import matplotlib.pyplot as plt

predictor = CycleToPeakPredictor()
predictor.load_all_data()

player_name = predictor.data_loader.gps_data['name'].unique()[0]
predictor.prepare_player_data(player_name, position='midfielder')
predictor.train_model(player_name)
prediction = predictor.predict_next_match(player_name)

# Generate charts
visualizer = PerformanceVisualizer()
evolution = predictor.get_performance_evolution(player_name)
cycle = predictor.get_training_cycle_summary(player_name)

if len(evolution) > 0:
    fig = visualizer.plot_performance_evolution(evolution, prediction['predicted_rating'])
    plt.savefig('test_evolution.png')
    print("Saved: test_evolution.png")

if len(cycle) > 0:
    fig = visualizer.plot_training_cycle(cycle)
    plt.savefig('test_cycle.png')
    print("Saved: test_cycle.png")
```

**Run it:**
```bash
python -c "from test_examples import example_3_with_visualization; example_3_with_visualization()"
```

---

## Example 4: Test Individual Components

**What it does:** Tests each module component separately

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

predictor = CycleToPeakPredictor()
predictor.load_all_data()

player_name = predictor.data_loader.gps_data['name'].unique()[0]

# Test DataLoader
player_gps = predictor.data_loader.get_player_gps_data(player_name)
print(f"GPS records: {len(player_gps)}")

# Test Training Cycle
cycle_data = predictor.cycle_calculator.get_training_cycle_features(player_name)
print(f"Cycle records: {len(cycle_data)}")

# Test Feature Engineer
physical_features = predictor.feature_engineer.extract_physical_features(cycle_data)
print(f"Features: {len(physical_features.columns)}")

# Test LSTM Predictor
print(f"Sequence length: {predictor.lstm_predictor.sequence_length}")
print(f"TensorFlow: {predictor.lstm_predictor.TENSORFLOW_AVAILABLE}")
```

**Run it:**
```bash
python -c "from test_examples import example_4_test_components; example_4_test_components()"
```

---

## Example 5: Test Different Positions

**What it does:** Tests predictions with different player positions

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

predictor = CycleToPeakPredictor()
predictor.load_all_data()

player_name = predictor.data_loader.gps_data['name'].unique()[0]

for position in ['defender', 'midfielder', 'forward']:
    predictor.prepare_player_data(player_name, position=position)
    predictor.train_model(player_name)
    prediction = predictor.predict_next_match(player_name)
    print(f"{position}: {prediction['match_readiness_score']:.2f}/10")
```

**Run it:**
```bash
python -c "from test_examples import example_5_different_positions; example_5_different_positions()"
```

---

## Example 6: Data Validation

**What it does:** Validates data quality and structure

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

predictor = CycleToPeakPredictor()
predictor.load_all_data()

gps_data = predictor.data_loader.gps_data

print(f"Total records: {len(gps_data)}")
print(f"Players: {gps_data['name'].nunique()}")
print(f"Date range: {gps_data['date'].min()} to {gps_data['date'].max()}")

# Check required columns
required = ['name', 'date', 'Total Distance (m)', 'Total Player Load']
for col in required:
    print(f"{col}: {'OK' if col in gps_data.columns else 'MISSING'}")
```

**Run it:**
```bash
python -c "from test_examples import example_6_data_validation; example_6_data_validation()"
```

---

## Example 7: Prediction Validation

**What it does:** Validates that predictions are in correct range (1-10)

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

predictor = CycleToPeakPredictor()
predictor.load_all_data()

players = predictor.data_loader.gps_data['name'].unique()[:10]
valid = 0
invalid = 0

for player_name in players:
    predictor.prepare_player_data(player_name, position='midfielder')
    predictor.train_model(player_name)
    prediction = predictor.predict_next_match(player_name)
    
    score = prediction['match_readiness_score']
    if 1.0 <= score <= 10.0:
        valid += 1
    else:
        invalid += 1
        print(f"INVALID: {player_name}: {score}/10")

print(f"Valid: {valid}, Invalid: {invalid}")
```

**Run it:**
```bash
python -c "from test_examples import example_7_prediction_validation; example_7_prediction_validation()"
```

---

## Example 8: Performance Test

**What it does:** Measures how fast predictions are generated

```python
from cycle_to_peak_predictor import CycleToPeakPredictor
import time

predictor = CycleToPeakPredictor()

start = time.time()
predictor.load_all_data()
print(f"Loading: {time.time() - start:.2f}s")

player_name = predictor.data_loader.gps_data['name'].unique()[0]

start = time.time()
predictor.prepare_player_data(player_name, position='midfielder')
print(f"Preparation: {time.time() - start:.2f}s")

start = time.time()
predictor.train_model(player_name)
print(f"Training: {time.time() - start:.2f}s")

start = time.time()
prediction = predictor.predict_next_match(player_name)
print(f"Prediction: {time.time() - start:.2f}s")
```

**Run it:**
```bash
python -c "from test_examples import example_8_performance_test; example_8_performance_test()"
```

---

## Running Examples from Command Line

### Run all examples:
```bash
python test_examples.py
```

### Run specific example:
```bash
python -c "from test_examples import example_1_basic_test; example_1_basic_test()"
```

### Run in Python interactive mode:
```python
>>> from test_examples import *
>>> example_1_basic_test()
>>> example_2_multiple_players()
```

---

## Expected Output

### Example 1 Output:
```
Player: Ahmed Al-Nakhli
Match Readiness Score: 3.18/10
Days Until Match: 0
Training Load: 182.57
```

### Example 2 Output:
```
Average Score: 4.14/10
Highest: 8.28/10
Lowest: 1.00/10
Ready (>=7): 1 players
At Risk (<5): 5 players
```

### Example 8 Output:
```
[1] Data Loading: 2.45 seconds
[2] Data Preparation: 0.32 seconds
[3] Model Training: 1.23 seconds
[4] Prediction: 0.05 seconds
Total Time: 4.05 seconds
```

---

## Tips

1. **Start with Example 1** - It's the simplest test
2. **Use Example 2** - To test multiple players quickly
3. **Use Example 6** - To check data quality first
4. **Use Example 8** - To measure performance
5. **Use Example 7** - To validate predictions are correct

---

## Troubleshooting

If an example fails:
1. Check that CSV files are in the folder
2. Ensure you have required dependencies installed
3. Check the error message for specific issues
4. Try Example 6 first to validate data

---

**All examples are ready to use!** 🚀

