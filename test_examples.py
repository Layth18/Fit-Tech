"""
Practical Examples for Testing the AI Model
Copy and run these examples to test different aspects of the AI module
"""

# ============================================================================
# EXAMPLE 1: Basic Test - Single Player Prediction
# ============================================================================

def example_1_basic_test():
    """Simple test: Predict for one player"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Single Player Test")
    print("=" * 70)
    
    from cycle_to_peak_predictor import CycleToPeakPredictor
    
    # Step 1: Initialize
    predictor = CycleToPeakPredictor()
    
    # Step 2: Load data
    print("\n[1] Loading data...")
    predictor.load_all_data()
    
    # Step 3: Get first available player
    players = predictor.data_loader.gps_data['name'].unique()
    player_name = players[0]
    print(f"[2] Testing with player: {player_name}")
    
    # Step 4: Prepare data
    print("[3] Preparing player data...")
    predictor.prepare_player_data(player_name, position='midfielder')
    
    # Step 5: Train model
    print("[4] Training model...")
    predictor.train_model(player_name)
    
    # Step 6: Predict
    print("[5] Generating prediction...")
    prediction = predictor.predict_next_match(player_name)
    
    # Step 7: Display results
    print("\n" + "-" * 70)
    print("RESULTS")
    print("-" * 70)
    print(f"Player: {prediction['player_name']}")
    print(f"Match Readiness Score: {prediction['match_readiness_score']}/10")
    print(f"Days Until Match: {prediction['days_until_match']}")
    print(f"Training Load: {prediction['recent_training_load']}")
    print("-" * 70)
    
    return prediction


# ============================================================================
# EXAMPLE 2: Test Multiple Players
# ============================================================================

def example_2_multiple_players():
    """Test predictions for multiple players"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Multiple Players Test")
    print("=" * 70)
    
    from cycle_to_peak_predictor import CycleToPeakPredictor
    import pandas as pd
    
    predictor = CycleToPeakPredictor()
    predictor.load_all_data()
    
    # Get first 5 players
    players = predictor.data_loader.gps_data['name'].unique()[:5]
    print(f"\nTesting {len(players)} players...")
    
    results = []
    
    for i, player_name in enumerate(players, 1):
        print(f"\n[{i}/{len(players)}] {player_name}")
        try:
            # Prepare, train, and predict
            predictor.prepare_player_data(player_name, position='midfielder')
            predictor.train_model(player_name)
            prediction = predictor.predict_next_match(player_name)
            results.append(prediction)
            
            score = prediction['match_readiness_score']
            status = "READY" if score >= 7 else "MODERATE" if score >= 5 else "AT RISK"
            print(f"  Score: {score:.2f}/10 [{status}]")
            
        except Exception as e:
            print(f"  ERROR: {str(e)[:50]}")
    
    # Summary
    if results:
        df = pd.DataFrame(results)
        print("\n" + "-" * 70)
        print("SUMMARY")
        print("-" * 70)
        print(f"Average Score: {df['match_readiness_score'].mean():.2f}/10")
        print(f"Highest: {df['match_readiness_score'].max():.2f}/10")
        print(f"Lowest: {df['match_readiness_score'].min():.2f}/10")
        print(f"Ready (>=7): {len(df[df['match_readiness_score'] >= 7])} players")
        print(f"At Risk (<5): {len(df[df['match_readiness_score'] < 5])} players")
    
    return results


# ============================================================================
# EXAMPLE 3: Test with Visualization
# ============================================================================

def example_3_with_visualization():
    """Test with chart generation"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Test with Visualization")
    print("=" * 70)
    
    from cycle_to_peak_predictor import CycleToPeakPredictor
    from visualization import PerformanceVisualizer
    import matplotlib.pyplot as plt
    
    predictor = CycleToPeakPredictor()
    predictor.load_all_data()
    
    # Get first player
    player_name = predictor.data_loader.gps_data['name'].unique()[0]
    print(f"\nTesting visualization for: {player_name}")
    
    # Prepare and train
    predictor.prepare_player_data(player_name, position='midfielder')
    predictor.train_model(player_name)
    prediction = predictor.predict_next_match(player_name)
    
    # Get data for charts
    evolution = predictor.get_performance_evolution(player_name)
    cycle = predictor.get_training_cycle_summary(player_name)
    
    # Create visualizer
    visualizer = PerformanceVisualizer()
    
    # Generate charts
    print("\nGenerating charts...")
    
    if len(evolution) > 0:
        fig1 = visualizer.plot_performance_evolution(
            evolution, 
            predicted_rating=prediction['predicted_rating']
        )
        if fig1:
            plt.savefig('example_performance_evolution.png', dpi=150, bbox_inches='tight')
            plt.close(fig1)
            print("[OK] Saved: example_performance_evolution.png")
    
    if len(cycle) > 0:
        fig2 = visualizer.plot_training_cycle(cycle)
        if fig2:
            plt.savefig('example_training_cycle.png', dpi=150, bbox_inches='tight')
            plt.close(fig2)
            print("[OK] Saved: example_training_cycle.png")
    
    print("\nVisualization test complete!")
    return True


# ============================================================================
# EXAMPLE 4: Test Model Components Individually
# ============================================================================

def example_4_test_components():
    """Test each component separately"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Test Individual Components")
    print("=" * 70)
    
    from cycle_to_peak_predictor import CycleToPeakPredictor
    
    predictor = CycleToPeakPredictor()
    predictor.load_all_data()
    
    player_name = predictor.data_loader.gps_data['name'].unique()[0]
    print(f"\nTesting components with player: {player_name}")
    
    # Test 1: Data Loader
    print("\n[1] Testing DataLoader...")
    player_gps = predictor.data_loader.get_player_gps_data(player_name)
    print(f"  GPS records: {len(player_gps)}")
    
    # Test 2: Training Cycle Calculator
    print("\n[2] Testing TrainingCycleCalculator...")
    cycle_data = predictor.cycle_calculator.get_training_cycle_features(player_name)
    print(f"  Cycle records: {len(cycle_data)}")
    if len(cycle_data) > 0:
        print(f"  Sample J_minus values: {cycle_data['J_minus'].head(5).tolist()}")
    
    # Test 3: Feature Engineer
    print("\n[3] Testing FeatureEngineer...")
    if len(cycle_data) > 0:
        physical_features = predictor.feature_engineer.extract_physical_features(cycle_data)
        print(f"  Physical features: {len(physical_features.columns)} columns")
        print(f"  Sample features: {list(physical_features.columns[:5])}")
    
    # Test 4: Performance Rating
    print("\n[4] Testing PerformanceRatingCalculator...")
    print(f"  Position: {predictor.rating_calculator.position}")
    print(f"  PCA available: {predictor.rating_calculator.pca is not None}")
    
    # Test 5: LSTM Predictor
    print("\n[5] Testing LSTMPredictor...")
    print(f"  Sequence length: {predictor.lstm_predictor.sequence_length}")
    print(f"  Features: {predictor.lstm_predictor.n_features}")
    print(f"  TensorFlow: {predictor.lstm_predictor.TENSORFLOW_AVAILABLE}")
    print(f"  Trained: {predictor.lstm_predictor.is_trained}")
    
    print("\n[OK] All components tested!")
    return True


# ============================================================================
# EXAMPLE 5: Test with Custom Position
# ============================================================================

def example_5_different_positions():
    """Test with different player positions"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Test Different Positions")
    print("=" * 70)
    
    from cycle_to_peak_predictor import CycleToPeakPredictor
    
    predictor = CycleToPeakPredictor()
    predictor.load_all_data()
    
    player_name = predictor.data_loader.gps_data['name'].unique()[0]
    
    positions = ['defender', 'midfielder', 'forward']
    
    for position in positions:
        print(f"\nTesting as {position}...")
        try:
            predictor.prepare_player_data(player_name, position=position)
            predictor.train_model(player_name)
            prediction = predictor.predict_next_match(player_name)
            print(f"  Score: {prediction['match_readiness_score']:.2f}/10")
        except Exception as e:
            print(f"  ERROR: {str(e)[:50]}")
    
    return True


# ============================================================================
# EXAMPLE 6: Test Data Validation
# ============================================================================

def example_6_data_validation():
    """Validate data quality and structure"""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Data Validation")
    print("=" * 70)
    
    from cycle_to_peak_predictor import CycleToPeakPredictor
    
    predictor = CycleToPeakPredictor()
    predictor.load_all_data()
    
    gps_data = predictor.data_loader.gps_data
    
    print("\n[1] GPS Data Validation:")
    print(f"  Total records: {len(gps_data)}")
    print(f"  Columns: {len(gps_data.columns)}")
    print(f"  Date range: {gps_data['date'].min()} to {gps_data['date'].max()}")
    print(f"  Players: {gps_data['name'].nunique()}")
    
    print("\n[2] Required Columns Check:")
    required_cols = ['name', 'date', 'Total Distance (m)', 'Total Player Load']
    for col in required_cols:
        exists = col in gps_data.columns
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {col}")
    
    print("\n[3] Data Quality:")
    print(f"  Missing values: {gps_data.isnull().sum().sum()}")
    print(f"  Duplicate records: {gps_data.duplicated().sum()}")
    
    print("\n[4] Sample Player Data:")
    player_name = gps_data['name'].unique()[0]
    player_data = gps_data[gps_data['name'] == player_name]
    print(f"  Player: {player_name}")
    print(f"  Records: {len(player_data)}")
    print(f"  Date range: {player_data['date'].min()} to {player_data['date'].max()}")
    
    return True


# ============================================================================
# EXAMPLE 7: Test Prediction Accuracy Range
# ============================================================================

def example_7_prediction_validation():
    """Validate that predictions are in correct range"""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Prediction Validation")
    print("=" * 70)
    
    from cycle_to_peak_predictor import CycleToPeakPredictor
    
    predictor = CycleToPeakPredictor()
    predictor.load_all_data()
    
    players = predictor.data_loader.gps_data['name'].unique()[:10]
    
    valid_predictions = 0
    invalid_predictions = 0
    
    for player_name in players:
        try:
            predictor.prepare_player_data(player_name, position='midfielder')
            predictor.train_model(player_name)
            prediction = predictor.predict_next_match(player_name)
            
            score = prediction['match_readiness_score']
            
            if 1.0 <= score <= 10.0:
                valid_predictions += 1
            else:
                invalid_predictions += 1
                print(f"[INVALID] {player_name}: {score}/10")
                
        except Exception as e:
            invalid_predictions += 1
            print(f"[ERROR] {player_name}: {str(e)[:50]}")
    
    print("\n" + "-" * 70)
    print("VALIDATION RESULTS")
    print("-" * 70)
    print(f"Valid predictions (1-10 range): {valid_predictions}")
    print(f"Invalid predictions: {invalid_predictions}")
    print(f"Success rate: {valid_predictions/(valid_predictions+invalid_predictions)*100:.1f}%")
    
    return valid_predictions > 0


# ============================================================================
# EXAMPLE 8: Quick Performance Test
# ============================================================================

def example_8_performance_test():
    """Test how fast predictions are generated"""
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Performance Test")
    print("=" * 70)
    
    from cycle_to_peak_predictor import CycleToPeakPredictor
    import time
    
    predictor = CycleToPeakPredictor()
    
    # Time data loading
    start = time.time()
    predictor.load_all_data()
    load_time = time.time() - start
    print(f"\n[1] Data Loading: {load_time:.2f} seconds")
    
    # Time prediction for one player
    player_name = predictor.data_loader.gps_data['name'].unique()[0]
    
    start = time.time()
    predictor.prepare_player_data(player_name, position='midfielder')
    prep_time = time.time() - start
    print(f"[2] Data Preparation: {prep_time:.2f} seconds")
    
    start = time.time()
    predictor.train_model(player_name)
    train_time = time.time() - start
    print(f"[3] Model Training: {train_time:.2f} seconds")
    
    start = time.time()
    prediction = predictor.predict_next_match(player_name)
    predict_time = time.time() - start
    print(f"[4] Prediction: {predict_time:.2f} seconds")
    
    total_time = load_time + prep_time + train_time + predict_time
    print(f"\nTotal Time: {total_time:.2f} seconds")
    print(f"Prediction Score: {prediction['match_readiness_score']:.2f}/10")
    
    return total_time


# ============================================================================
# MAIN: Run All Examples
# ============================================================================

def run_all_examples():
    """Run all test examples"""
    print("\n" + "=" * 70)
    print("RUNNING ALL TEST EXAMPLES")
    print("=" * 70)
    
    examples = [
        ("Basic Test", example_1_basic_test),
        ("Multiple Players", example_2_multiple_players),
        ("With Visualization", example_3_with_visualization),
        ("Test Components", example_4_test_components),
        ("Different Positions", example_5_different_positions),
        ("Data Validation", example_6_data_validation),
        ("Prediction Validation", example_7_prediction_validation),
        ("Performance Test", example_8_performance_test),
    ]
    
    results = {}
    
    for name, func in examples:
        try:
            print(f"\n{'='*70}")
            result = func()
            results[name] = True
            print(f"\n[OK] {name} completed successfully")
        except Exception as e:
            results[name] = False
            print(f"\n[FAIL] {name} failed: {str(e)[:100]}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for name, success in results.items():
        status = "[PASSED]" if success else "[FAILED]"
        print(f"{name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\nTotal: {passed}/{total} examples passed")
    
    return results


if __name__ == "__main__":
    # You can run individual examples or all of them
    
    # Option 1: Run a specific example
    # example_1_basic_test()
    
    # Option 2: Run all examples
    run_all_examples()

