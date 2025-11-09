"""
Example Usage Script for Cycle-to-Peak Performance Predictor
Demonstrates how to use the AI system to predict player performance
"""

import pandas as pd
from cycle_to_peak_predictor import CycleToPeakPredictor
from visualization import PerformanceVisualizer
import matplotlib.pyplot as plt


def example_single_player():
    """Example: Predict performance for a single player"""
    print("=" * 70)
    print("EXAMPLE 1: Single Player Performance Prediction")
    print("=" * 70)
    
    # Initialize predictor
    predictor = CycleToPeakPredictor()
    
    # Load data
    predictor.load_all_data()
    
    # Get available players
    if predictor.data_loader.gps_data is not None:
        available_players = predictor.data_loader.gps_data['name'].unique()
        print(f"\nFound {len(available_players)} players in dataset")
        
        if len(available_players) > 0:
            # Select first player
            player_name = available_players[0]
            print(f"\nAnalyzing player: {player_name}")
            
            # Prepare player data
            player_data = predictor.prepare_player_data(player_name, position='midfielder')
            
            if len(player_data) > 0:
                # Train model
                print("\nTraining prediction model...")
                history = predictor.train_model(player_name)
                
                # Predict next match
                print("\nGenerating prediction...")
                prediction = predictor.predict_next_match(player_name)
                
                # Display results
                print("\n" + "-" * 70)
                print("PREDICTION RESULTS")
                print("-" * 70)
                print(f"Player Name: {prediction['player_name']}")
                print(f"Match Readiness Score: {prediction['match_readiness_score']}/10")
                print(f"Days Until Next Match: {prediction['days_until_match']}")
                print(f"Recent Training Load: {prediction['recent_training_load']}")
                print(f"Prediction Date: {prediction['prediction_date']}")
                
                # Get performance evolution
                evolution = predictor.get_performance_evolution(player_name)
                if len(evolution) > 0:
                    print(f"\nHistorical Performance (Last 5 matches):")
                    print(evolution[['date', 'performance_rating']].tail(5).to_string(index=False))
                
                # Create visualizations
                print("\nGenerating visualizations...")
                visualizer = PerformanceVisualizer()
                
                # Performance evolution chart
                if len(evolution) > 0:
                    fig1 = visualizer.plot_performance_evolution(
                        evolution, 
                        predicted_rating=prediction['predicted_rating']
                    )
                    if fig1:
                        plt.savefig('performance_evolution.png', dpi=300, bbox_inches='tight')
                        print("Saved: performance_evolution.png")
                
                # Training cycle chart
                cycle = predictor.get_training_cycle_summary(player_name)
                if len(cycle) > 0:
                    fig2 = visualizer.plot_training_cycle(cycle)
                    if fig2:
                        plt.savefig('training_cycle.png', dpi=300, bbox_inches='tight')
                        print("Saved: training_cycle.png")
                
                # Summary report
                if len(evolution) > 0 and len(cycle) > 0:
                    fig3 = visualizer.create_summary_report(
                        player_name, prediction, evolution, cycle
                    )
                    if fig3:
                        plt.savefig('player_summary_report.png', dpi=300, bbox_inches='tight')
                        print("Saved: player_summary_report.png")
                
                print("\n" + "=" * 70)
                print("Analysis complete!")
                print("=" * 70)


def example_team_overview():
    """Example: Get match readiness for entire team"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Team Match Readiness Overview")
    print("=" * 70)
    
    # Initialize predictor
    predictor = CycleToPeakPredictor()
    
    # Load data
    predictor.load_all_data()
    
    # Get available players (limit to first 10 for demo)
    if predictor.data_loader.gps_data is not None:
        available_players = predictor.data_loader.gps_data['name'].unique()[:10]
        print(f"\nAnalyzing {len(available_players)} players...")
        
        predictions = []
        
        for player_name in available_players:
            try:
                # Prepare data
                player_data = predictor.prepare_player_data(player_name, position='midfielder')
                
                if len(player_data) > 0:
                    # Train model (quick training)
                    predictor.train_model(player_name)
                    
                    # Predict
                    prediction = predictor.predict_next_match(player_name)
                    predictions.append(prediction)
                    
                    print(f"  [OK] {player_name}: {prediction['match_readiness_score']:.2f}/10")
            except Exception as e:
                print(f"  [ERROR] {player_name}: Error - {str(e)}")
        
        if len(predictions) > 0:
            # Create team dashboard
            visualizer = PerformanceVisualizer()
            fig = visualizer.plot_match_readiness_dashboard(predictions)
            
            if fig:
                plt.savefig('team_readiness_dashboard.png', dpi=300, bbox_inches='tight')
                print(f"\nSaved: team_readiness_dashboard.png")
                
                # Display summary
                df = pd.DataFrame(predictions)
                print("\n" + "-" * 70)
                print("TEAM READINESS SUMMARY")
                print("-" * 70)
                print(f"Average Readiness Score: {df['match_readiness_score'].mean():.2f}/10")
                print(f"Highest: {df.loc[df['match_readiness_score'].idxmax(), 'player_name']} "
                      f"({df['match_readiness_score'].max():.2f}/10)")
                print(f"Lowest: {df.loc[df['match_readiness_score'].idxmin(), 'player_name']} "
                      f"({df['match_readiness_score'].min():.2f}/10)")
                print(f"\nPlayers Ready (>=7.0): {len(df[df['match_readiness_score'] >= 7.0])}")
                print(f"Players At Risk (<5.0): {len(df[df['match_readiness_score'] < 5.0])}")
        
        print("\n" + "=" * 70)
        print("Team analysis complete!")
        print("=" * 70)


def main():
    """Run examples"""
    print("\n" + "=" * 70)
    print("CYCLE-TO-PEAK PERFORMANCE PREDICTOR - EXAMPLE USAGE")
    print("=" * 70)
    
    # Example 1: Single player
    try:
        example_single_player()
    except Exception as e:
        print(f"Error in single player example: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Team overview
    try:
        example_team_overview()
    except Exception as e:
        print(f"Error in team overview example: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

