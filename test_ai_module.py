"""
Test Script for AI Module
Comprehensive testing suite for the Cycle-to-Peak Performance Predictor
"""

import pandas as pd
from cycle_to_peak_predictor import CycleToPeakPredictor
from visualization import PerformanceVisualizer
import matplotlib.pyplot as plt
import traceback
import os


def test_data_loading():
    """Test 1: Verify data loading works correctly"""
    print("=" * 70)
    print("TEST 1: Data Loading")
    print("=" * 70)
    
    try:
        predictor = CycleToPeakPredictor()
        
        print("\nLoading data files...")
        predictor.load_all_data()
        
        # Check GPS data
        if predictor.data_loader.gps_data is None or len(predictor.data_loader.gps_data) == 0:
            print("[FAIL] GPS data not loaded")
            return False, None
        
        print(f"[OK] GPS data loaded: {len(predictor.data_loader.gps_data)} records")
        
        # Check match data
        if predictor.data_loader.match_data is not None:
            print(f"[OK] Match data loaded: {len(predictor.data_loader.match_data)} records")
        else:
            print("[WARNING] Match data not loaded (optional)")
        
        # Check player data
        if predictor.data_loader.player_data is not None:
            print(f"[OK] Player data loaded: {len(predictor.data_loader.player_data)} records")
        else:
            print("[WARNING] Player data not loaded (optional)")
        
        # List available players
        available_players = predictor.data_loader.gps_data['name'].unique()
        print(f"\n[OK] Found {len(available_players)} players in dataset")
        print(f"Sample players: {list(available_players[:5])}")
        
        return True, predictor
        
    except Exception as e:
        print(f"[FAIL] Error loading data: {e}")
        traceback.print_exc()
        return False, None


def test_single_player_prediction(predictor, player_name=None):
    """Test 2: Test prediction for a single player"""
    print("\n" + "=" * 70)
    print("TEST 2: Single Player Prediction")
    print("=" * 70)
    
    try:
        # Get available players if not specified
        if player_name is None:
            available_players = predictor.data_loader.gps_data['name'].unique()
            if len(available_players) == 0:
                print("[FAIL] No players found in dataset")
                return False
            player_name = available_players[0]
            print(f"Testing with player: {player_name}")
        
        # Check player data availability
        player_gps = predictor.data_loader.get_player_gps_data(player_name)
        print(f"\n[OK] Found {len(player_gps)} GPS records for {player_name}")
        
        if len(player_gps) < 15:
            print(f"[WARNING] Only {len(player_gps)} records found. Need at least 15 for optimal prediction.")
        
        # Prepare player data
        print("\nPreparing player data...")
        player_data = predictor.prepare_player_data(player_name, position='midfielder')
        
        if len(player_data) == 0:
            print("[FAIL] Failed to prepare player data")
            return False
        
        print(f"[OK] Player data prepared:")
        print(f"  - GPS records: {len(player_data['gps_data'])}")
        print(f"  - Match records: {len(player_data['match_data'])}")
        print(f"  - Combined features: {len(player_data['combined_features'])}")
        
        # Train model
        print("\nTraining prediction model...")
        history = predictor.train_model(player_name)
        
        if len(history) == 0:
            print("[WARNING] Model training returned empty history (may have used fallback)")
        else:
            print("[OK] Model trained successfully")
        
        # Make prediction
        print("\nGenerating prediction...")
        prediction = predictor.predict_next_match(player_name)
        
        # Display results
        print("\n" + "-" * 70)
        print("PREDICTION RESULTS")
        print("-" * 70)
        print(f"Player Name: {prediction['player_name']}")
        print(f"Match Readiness Score: {prediction['match_readiness_score']}/10")
        print(f"Predicted Rating: {prediction['predicted_rating']}/10")
        print(f"Days Until Next Match: {prediction['days_until_match']}")
        print(f"Recent Training Load: {prediction['recent_training_load']}")
        print(f"Prediction Date: {prediction['prediction_date']}")
        
        # Validate prediction
        score = prediction['match_readiness_score']
        if 1.0 <= score <= 10.0:
            print(f"\n[OK] Prediction score is valid (1-10 range)")
        else:
            print(f"\n[WARNING] Prediction score out of range: {score}")
        
        # Get performance evolution
        evolution = predictor.get_performance_evolution(player_name)
        if len(evolution) > 0:
            print(f"\nHistorical Performance (Last 5 matches):")
            print(evolution[['date', 'performance_rating']].tail(5).to_string(index=False))
        else:
            print("\n[WARNING] No historical performance data available")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error in prediction: {e}")
        traceback.print_exc()
        return False


def test_multiple_players(predictor, max_players=5):
    """Test 3: Test predictions for multiple players"""
    print("\n" + "=" * 70)
    print("TEST 3: Multiple Players Prediction")
    print("=" * 70)
    
    try:
        available_players = predictor.data_loader.gps_data['name'].unique()[:max_players]
        print(f"Testing {len(available_players)} players...")
        
        results = []
        successful = 0
        failed = 0
        
        for i, player_name in enumerate(available_players, 1):
            print(f"\n[{i}/{len(available_players)}] Processing: {player_name}")
            try:
                # Prepare and train
                player_data = predictor.prepare_player_data(player_name, position='midfielder')
                
                if len(player_data) > 0 and len(player_data['combined_features']) >= 15:
                    predictor.train_model(player_name)
                    prediction = predictor.predict_next_match(player_name)
                    results.append(prediction)
                    successful += 1
                    print(f"  [OK] Readiness: {prediction['match_readiness_score']:.2f}/10")
                else:
                    print(f"  [WARNING] Insufficient data (need at least 15 records)")
                    failed += 1
            except Exception as e:
                print(f"  [FAIL] Error: {str(e)[:50]}")
                failed += 1
        
        # Summary
        print("\n" + "-" * 70)
        print("SUMMARY")
        print("-" * 70)
        print(f"Successful predictions: {successful}")
        print(f"Failed: {failed}")
        
        if len(results) > 0:
            df = pd.DataFrame(results)
            print(f"\nAverage Readiness Score: {df['match_readiness_score'].mean():.2f}/10")
            print(f"Highest: {df['match_readiness_score'].max():.2f}/10")
            print(f"Lowest: {df['match_readiness_score'].min():.2f}/10")
        
        return successful > 0
        
    except Exception as e:
        print(f"[FAIL] Error in multiple players test: {e}")
        traceback.print_exc()
        return False


def test_visualization(predictor):
    """Test 4: Test visualization generation"""
    print("\n" + "=" * 70)
    print("TEST 4: Visualization")
    print("=" * 70)
    
    try:
        available_players = predictor.data_loader.gps_data['name'].unique()
        if len(available_players) == 0:
            print("[FAIL] No players available for visualization")
            return False
        
        player_name = available_players[0]
        print(f"Testing visualization for: {player_name}")
        
        # Prepare and train
        predictor.prepare_player_data(player_name, position='midfielder')
        predictor.train_model(player_name)
        prediction = predictor.predict_next_match(player_name)
        
        # Get data for visualization
        evolution = predictor.get_performance_evolution(player_name)
        cycle = predictor.get_training_cycle_summary(player_name)
        
        # Create visualizer
        visualizer = PerformanceVisualizer()
        
        # Test performance evolution plot
        if len(evolution) > 0:
            fig1 = visualizer.plot_performance_evolution(
                evolution, 
                predicted_rating=prediction['predicted_rating']
            )
            if fig1:
                plt.savefig('test_performance_evolution.png', dpi=150, bbox_inches='tight')
                plt.close(fig1)
                print("[OK] Performance evolution chart saved: test_performance_evolution.png")
            else:
                print("[WARNING] Failed to create performance evolution chart")
        else:
            print("[WARNING] No evolution data for visualization")
        
        # Test training cycle plot
        if len(cycle) > 0:
            fig2 = visualizer.plot_training_cycle(cycle)
            if fig2:
                plt.savefig('test_training_cycle.png', dpi=150, bbox_inches='tight')
                plt.close(fig2)
                print("[OK] Training cycle chart saved: test_training_cycle.png")
            else:
                print("[WARNING] Failed to create training cycle chart")
        else:
            print("[WARNING] No cycle data for visualization")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error in visualization test: {e}")
        traceback.print_exc()
        return False


def test_model_components():
    """Test 5: Test individual model components"""
    print("\n" + "=" * 70)
    print("TEST 5: Model Components")
    print("=" * 70)
    
    try:
        predictor = CycleToPeakPredictor()
        predictor.load_all_data()
        
        # Test data loader
        print("\n[1] Testing DataLoader...")
        assert predictor.data_loader is not None, "DataLoader not initialized"
        print("  [OK] DataLoader initialized")
        
        # Test cycle calculator
        print("\n[2] Testing TrainingCycleCalculator...")
        assert predictor.cycle_calculator is not None, "TrainingCycleCalculator not initialized"
        print("  [OK] TrainingCycleCalculator initialized")
        
        # Test feature engineer
        print("\n[3] Testing FeatureEngineer...")
        assert predictor.feature_engineer is not None, "FeatureEngineer not initialized"
        print("  [OK] FeatureEngineer initialized")
        
        # Test rating calculator
        print("\n[4] Testing PerformanceRatingCalculator...")
        assert predictor.rating_calculator is not None, "PerformanceRatingCalculator not initialized"
        print("  [OK] PerformanceRatingCalculator initialized")
        
        # Test LSTM predictor
        print("\n[5] Testing LSTMPredictor...")
        assert predictor.lstm_predictor is not None, "LSTMPredictor not initialized"
        print("  [OK] LSTMPredictor initialized")
        print(f"  - Sequence length: {predictor.lstm_predictor.sequence_length}")
        print(f"  - Features: {predictor.lstm_predictor.n_features}")
        print(f"  - TensorFlow available: {predictor.lstm_predictor.TENSORFLOW_AVAILABLE}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error in component test: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("AI MODULE TEST SUITE")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Data Loading
    success, predictor = test_data_loading()
    results['Data Loading'] = success
    
    if not success:
        print("\n[FAIL] Cannot proceed without data. Please check your CSV files.")
        return
    
    # Test 5: Model Components (quick test)
    results['Model Components'] = test_model_components()
    
    # Test 2: Single Player Prediction
    results['Single Player'] = test_single_player_prediction(predictor)
    
    # Test 3: Multiple Players
    results['Multiple Players'] = test_multiple_players(predictor, max_players=3)
    
    # Test 4: Visualization
    results['Visualization'] = test_visualization(predictor)
    
    # Final Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, result in results.items():
        status = "[PASSED]" if result else "[FAILED]"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n[SUCCESS] All tests passed! The AI module is working correctly.")
    else:
        print(f"\n[WARNING] {total_tests - total_passed} test(s) failed. Please review the errors above.")
    
    print("\n" + "=" * 70)
    print("Testing complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()

