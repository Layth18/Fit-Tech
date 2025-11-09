# Cycle-to-Peak Performance Predictor

An advanced AI system that predicts football player performance by analyzing training cycles, GPS data, and match statistics. The system uses LSTM neural networks to forecast a player's "Match Readiness Score" based on their training periodization and historical performance.

## 🎯 Project Overview

This AI model predicts the evolution of a football player's performance by holistically analyzing:
- **Physical Load**: GPS tracking data from training sessions and matches
- **Technical Performance**: Wyscout match statistics and event data
- **Training Cycles**: Periodization analysis (J- days until next match)

The core innovation is modeling the training cycle between matches as a key predictor for performance in the next match.

## 📋 Features

### Core Functionality
1. **Training Cycle Calculation**: Automatically calculates J- days (days until next match) for each training session
2. **Advanced Feature Engineering**: Extracts physical and technical metrics from GPS and Wyscout data
3. **Performance Rating System**: Creates composite Match Performance Ratings (1-10 scale) using PCA-weighted metrics
4. **LSTM Prediction Model**: Uses Long Short-Term Memory networks to predict future match performance
5. **Visualization Dashboard**: Generates charts and reports for performance analysis

### Key Capabilities
- Predict Match Readiness Score for individual players
- Track performance evolution over time
- Visualize training cycles and physical load distribution
- Generate team-wide readiness overviews
- Identify players at risk of fatigue or poor performance

## 📁 Project Structure

```
hakaton/
├── data_loader.py              # Data loading and preprocessing
├── training_cycle.py           # Training cycle calculation (J- days)
├── feature_engineering.py      # Feature extraction from GPS/Wyscout
├── performance_rating.py       # Historical performance rating system
├── lstm_predictor.py           # LSTM model for predictions
├── cycle_to_peak_predictor.py  # Main pipeline (integrates all components)
├── visualization.py            # Chart and report generation
├── example_usage.py            # Example scripts demonstrating usage
├── test_ai_module.py           # Test suite for validation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Required data files:
  - `training_gps.csv` - GPS training data
  - `matchs_gps.csv` - GPS match data
  - `wyscout_matchs.csv` - Match-level Wyscout data
  - `wyscout_players_outfield.csv` - Player-level Wyscout data

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Ensure data files are in the project directory**

## 💻 Usage

### Basic Usage - Single Player Prediction

```python
from cycle_to_peak_predictor import CycleToPeakPredictor

# Initialize predictor
predictor = CycleToPeakPredictor()

# Load data
predictor.load_all_data()

# Prepare data for a player
player_data = predictor.prepare_player_data(
    player_name="Ahmed Al-Nakhli",
    position="midfielder"  # 'defender', 'midfielder', or 'forward'
)

# Train the prediction model
predictor.train_model("Ahmed Al-Nakhli")

# Predict next match performance
prediction = predictor.predict_next_match("Ahmed Al-Nakhli")

print(f"Match Readiness Score: {prediction['match_readiness_score']}/10")
print(f"Days Until Match: {prediction['days_until_match']}")
```

### Run Example Scripts

```bash
# Run main pipeline with example
python cycle_to_peak_predictor.py

# Run comprehensive examples
python example_usage.py

# Run test suite to validate functionality
python test_ai_module.py
```

### Generate Visualizations

```python
from visualization import PerformanceVisualizer

visualizer = PerformanceVisualizer()

# Performance evolution chart
evolution = predictor.get_performance_evolution("Ahmed Al-Nakhli")
fig = visualizer.plot_performance_evolution(
    evolution, 
    predicted_rating=prediction['predicted_rating']
)
plt.savefig('performance_evolution.png')

# Training cycle visualization
cycle = predictor.get_training_cycle_summary("Ahmed Al-Nakhli")
fig = visualizer.plot_training_cycle(cycle)
plt.savefig('training_cycle.png')
```

## 🔬 Methodology

### Three-Pillar Approach

#### Pillar 1: Training Cycle Calculation
- Classifies each day as 'Match Day', 'Training Day', or 'Rest Day'
- Calculates J- (days until next match) for periodization analysis
- Maps microcycles between matches

#### Pillar 2: Advanced Feature Engineering

**Physical Features (from GPS)**:
- Volume: Total Distance Covered
- Intensity: High-Speed Running (>19.8 km/h), Sprint Distance (>25.2 km/h)
- Explosiveness: Accelerations/Decelerations (>3m/s²)
- Load: Player Load (accelerometer-based)
- Heart Rate: Average and Maximum HR

**Technical Features (from Wyscout)**:
- Position-specific KPIs:
  - **Defenders**: Tackles won %, Interceptions, Clearances
  - **Midfielders**: Passing accuracy %, Progressive passes, Key passes
  - **Forwards**: Shots, Goals, xG, Successful dribbles

#### Pillar 3: AI-Powered Prediction

**Stage 1: Historical Performance Rating**
- Creates composite Match Performance Rating (1-10 scale)
- Uses Z-score standardization to compare against position averages
- Applies PCA to determine feature importance weights

**Stage 2: LSTM Performance Prediction**
- Input: Time series of last 15 days (training load, performance ratings, context)
- Model: LSTM neural network with dropout regularization
- Output: Predicted Match Performance Rating for next match
- Learns patterns between training periodization and performance

## 📊 Output Format

### Prediction Dictionary
```python
{
    'player_name': 'Ahmed Al-Nakhli',
    'predicted_rating': 7.85,
    'match_readiness_score': 7.85,  # Same as predicted_rating
    'days_until_match': 3,
    'recent_training_load': 245.6,
    'prediction_date': '2025-01-15'
}
```

### Performance Evolution DataFrame
- `date`: Match date
- `performance_rating`: Historical performance rating (1-10)
- `match`: Match identifier

### Training Cycle Summary DataFrame
- `date`: Training date
- `J_minus`: Days until next match
- `event_type`: 'Match Day', 'Training Day', or 'Rest Day'
- `player_load`: Physical load metric

## 🎨 Visualization Features

1. **Performance Evolution Chart**: Line graph showing historical ratings and predicted future rating
2. **Training Cycle Visualizer**: Bar chart showing daily physical load in the cycle leading to a match
3. **Team Readiness Dashboard**: Overview ranking all players by predicted readiness score
4. **Summary Report**: Comprehensive multi-panel report for individual players

## 🔧 Configuration

### Model Parameters

In `lstm_predictor.py`, you can adjust:
- `sequence_length`: Number of days in input sequence (default: 15)
- `n_features`: Number of features used (default: 20)
- `epochs`: Training epochs (default: 50)
- `batch_size`: Batch size for training (default: 32)

### Position-Specific Features

The system automatically selects relevant features based on player position:
- **Defender**: Defensive duels, interceptions, aerial duels
- **Midfielder**: Passing accuracy, progressive passes, key passes
- **Forward**: Goals, shots, xG, dribbles, offensive duels

## 📈 Model Performance

The LSTM model:
- Uses dropout (0.2) for regularization
- Implements early stopping via validation split
- Falls back to linear regression if TensorFlow is unavailable
- Normalizes predictions to 1-10 scale

## 🛠️ Troubleshooting

### Common Issues

1. **No GPS data found for player**
   - Ensure player name matches exactly in the CSV files
   - Check that `training_gps.csv` contains the player's data

2. **Insufficient data for training**
   - Need at least 15 days of data (sequence_length)
   - Model will use available data and pad if necessary

3. **TensorFlow not available**
   - System automatically falls back to linear regression
   - Install TensorFlow: `pip install tensorflow`

4. **Missing columns in data**
   - System handles missing columns gracefully
   - Missing metrics default to 0

## 📝 Data Requirements

### GPS Data (`training_gps.csv`)
Required columns:
- `name`: Player name
- `date`: Training/match date
- `Total Distance (m)`: Total distance covered
- `Total Player Load`: Player load metric
- `HS Distance (m)`: High-speed distance
- `Sprint`: Sprint distance
- `Accel + Decel Efforts`: Acceleration/deceleration efforts

### Wyscout Data
Required columns:
- `player`: Player name
- `date`: Match date
- Position-specific metrics (varies by position)

## 🎯 Use Cases

1. **Coaching Decisions**: Optimize training loads to ensure players peak for key matches
2. **Team Selection**: Make data-driven decisions on starting lineups
3. **Injury Prevention**: Flag players with training patterns indicating burnout risk
4. **Performance Monitoring**: Track player form and evolution over time

## 🔮 Future Enhancements

- Integration with real-time data feeds
- Web dashboard interface
- Multi-player comparison tools
- Advanced injury risk prediction
- Opponent strength analysis integration
- Competition importance weighting

## 📄 License

This project is developed for the hackathon competition.

## 👥 Authors

Developed as part of the Cycle-to-Peak Performance Predictor project.

---

**Note**: This system requires historical GPS and Wyscout data to function. Ensure all data files are properly formatted and contain the required columns.


