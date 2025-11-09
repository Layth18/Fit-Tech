"""
Cycle-to-Peak Performance Predictor - Main Pipeline
Integrates all components to predict player match performance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

from data_loader import DataLoader
from training_cycle import TrainingCycleCalculator
from feature_engineering import FeatureEngineer
from performance_rating import PerformanceRatingCalculator
from lstm_predictor import LSTMPredictor


class CycleToPeakPredictor:
    """Main class for Cycle-to-Peak Performance Prediction"""
    
    def __init__(self, data_dir: str = "."):
        self.data_loader = DataLoader(data_dir)
        self.cycle_calculator = TrainingCycleCalculator(self.data_loader)
        self.feature_engineer = FeatureEngineer()
        self.rating_calculator = PerformanceRatingCalculator()
        self.lstm_predictor = LSTMPredictor(sequence_length=15, n_features=20)
        
        # Data storage
        self.player_data_cache = {}
        
    def load_all_data(self):
        """Load all required data files"""
        print("Loading all data files...")
        self.data_loader.load_gps_data("training_gps.csv")
        self.data_loader.load_match_data("wyscout_matchs.csv")
        self.data_loader.load_player_data("wyscout_players_outfield.csv")
        print("Data loading complete!")
    
    def prepare_player_data(self, player_name: str, position: str = 'midfielder',
                           team_name: Optional[str] = None) -> Dict:
        """
        Prepare all data for a specific player
        Returns dictionary with processed data
        """
        print(f"\nPreparing data for player: {player_name}")
        
        # Get GPS data with training cycles
        gps_with_cycle = self.cycle_calculator.get_training_cycle_features(
            player_name, team_name
        )
        
        if len(gps_with_cycle) == 0:
            print(f"No GPS data found for {player_name}")
            return {}
        
        # Get player match data
        player_matches = self.data_loader.get_player_match_data(player_name)
        
        # Extract features
        physical_features = self.feature_engineer.extract_physical_features(gps_with_cycle)
        technical_features = self.feature_engineer.extract_technical_features(
            player_matches, position
        )
        
        # Calculate performance ratings for matches
        if len(player_matches) > 0:
            # Match physical features with match dates
            match_physical = self._match_physical_to_dates(
                gps_with_cycle, player_matches
            )
            
            if len(match_physical) > 0:
                match_technical = technical_features.iloc[:len(match_physical)]
                if len(match_technical) < len(match_physical):
                    # Pad with zeros
                    padding = pd.DataFrame(0, index=range(len(match_physical) - len(match_technical)),
                                         columns=match_technical.columns)
                    match_technical = pd.concat([match_technical, padding], ignore_index=True)
                
                performance_ratings = self.rating_calculator.calculate_match_rating(
                    match_physical, match_technical, position
                )
            else:
                performance_ratings = pd.Series([5.0] * len(player_matches))
        else:
            performance_ratings = pd.Series([])
        
        # Combine all features
        combined_features = self.feature_engineer.combine_features(
            physical_features, technical_features, gps_with_cycle
        )
        
        # Add performance ratings to combined features where available
        if len(performance_ratings) > 0 and len(combined_features) >= len(performance_ratings):
            combined_features['performance_rating'] = 0
            # Try to align ratings with match dates
            if 'date' in combined_features.columns and 'date' in player_matches.columns:
                match_dates = set(player_matches['date'].dt.date)
                combined_features['performance_rating'] = combined_features.apply(
                    lambda row: performance_ratings.iloc[0] if pd.to_datetime(row['date']).date() in match_dates else 0,
                    axis=1
                )
        
        # Store in cache
        self.player_data_cache[player_name] = {
            'gps_data': gps_with_cycle,
            'match_data': player_matches,
            'physical_features': physical_features,
            'technical_features': technical_features,
            'performance_ratings': performance_ratings,
            'combined_features': combined_features,
            'position': position
        }
        
        return self.player_data_cache[player_name]
    
    def _match_physical_to_dates(self, gps_data: pd.DataFrame, match_data: pd.DataFrame) -> pd.DataFrame:
        """Match physical features to match dates"""
        if len(match_data) == 0:
            return pd.DataFrame()
        
        match_dates = set(match_data['date'].dt.date)
        match_gps = gps_data[gps_data['date'].dt.date.isin(match_dates)]
        
        return match_gps
    
    def train_model(self, player_name: str) -> Dict:
        """
        Train LSTM model for a specific player
        """
        if player_name not in self.player_data_cache:
            print(f"Player data not prepared. Preparing now...")
            self.prepare_player_data(player_name)
        
        player_data = self.player_data_cache[player_name]
        combined_features = player_data['combined_features']
        
        if len(combined_features) < self.lstm_predictor.sequence_length:
            print(f"Insufficient data for training. Need at least {self.lstm_predictor.sequence_length} records.")
            return {}
        
        # Select feature columns
        feature_cols = [col for col in combined_features.select_dtypes(include=[np.number]).columns
                       if col not in ['performance_rating', 'J_minus', 'cycle_id']]
        feature_cols = feature_cols[:self.lstm_predictor.n_features]  # Limit features
        
        # Add performance rating if not present
        if 'performance_rating' not in combined_features.columns:
            # Use a default rating based on physical load
            if 'player_load' in combined_features.columns:
                combined_features['performance_rating'] = (
                    1 + 9 * (combined_features['player_load'] - combined_features['player_load'].min()) /
                    (combined_features['player_load'].max() - combined_features['player_load'].min() + 1e-6)
                )
            else:
                combined_features['performance_rating'] = 5.0
        
        # Prepare sequences
        X, y = self.lstm_predictor.prepare_sequences(
            combined_features,
            target_col='performance_rating',
            feature_cols=feature_cols
        )
        
        if len(X) == 0:
            print("No sequences prepared. Cannot train model.")
            return {}
        
        print(f"Training model with {len(X)} sequences...")
        
        # Train model
        history = self.lstm_predictor.train(
            X, y,
            validation_split=0.2,
            epochs=50,
            batch_size=min(32, len(X)),
            verbose=0
        )
        
        print("Model training complete!")
        return history
    
    def predict_next_match(self, player_name: str) -> Dict:
        """
        Predict performance rating for next match
        Returns dictionary with prediction and context
        """
        if player_name not in self.player_data_cache:
            print(f"Player data not prepared. Preparing now...")
            self.prepare_player_data(player_name)
        
        player_data = self.player_data_cache[player_name]
        combined_features = player_data['combined_features']
        
        # Get recent training cycle data (last 15 days or available data)
        recent_data = combined_features.tail(self.lstm_predictor.sequence_length).copy()
        
        # Select feature columns
        feature_cols = [col for col in recent_data.select_dtypes(include=[np.number]).columns
                       if col not in ['performance_rating', 'J_minus', 'cycle_id']]
        feature_cols = feature_cols[:self.lstm_predictor.n_features]
        
        # Predict
        try:
            predicted_rating = self.lstm_predictor.predict_next_match(recent_data, feature_cols)
        except Exception as e:
            print(f"Prediction error: {e}. Using fallback method.")
            # Fallback: use average of recent performance
            if 'performance_rating' in combined_features.columns:
                recent_ratings = combined_features['performance_rating'].tail(5)
                predicted_rating = recent_ratings.mean() if len(recent_ratings) > 0 else 5.0
            else:
                predicted_rating = 5.0
        
        # Get training cycle context
        if len(recent_data) > 0:
            j_minus = recent_data['J_minus'].iloc[-1] if 'J_minus' in recent_data.columns else None
            recent_load = recent_data['player_load'].mean() if 'player_load' in recent_data.columns else 0
        else:
            j_minus = None
            recent_load = 0
        
        result = {
            'player_name': player_name,
            'predicted_rating': round(predicted_rating, 2),
            'match_readiness_score': round(predicted_rating, 2),  # Same as rating
            'days_until_match': int(j_minus) if j_minus is not None else None,
            'recent_training_load': round(recent_load, 2),
            'prediction_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        return result
    
    def get_performance_evolution(self, player_name: str) -> pd.DataFrame:
        """
        Get historical performance evolution for visualization
        """
        if player_name not in self.player_data_cache:
            self.prepare_player_data(player_name)
        
        player_data = self.player_data_cache[player_name]
        match_data = player_data['match_data']
        ratings = player_data['performance_ratings']
        
        if len(match_data) == 0 or len(ratings) == 0:
            return pd.DataFrame()
        
        evolution = pd.DataFrame({
            'date': match_data['date'].values[:len(ratings)],
            'performance_rating': ratings.values,
            'match': match_data['match'].values[:len(ratings)] if 'match' in match_data.columns else ['Unknown'] * len(ratings)
        })
        
        return evolution
    
    def get_training_cycle_summary(self, player_name: str) -> pd.DataFrame:
        """
        Get training cycle summary for visualization
        """
        if player_name not in self.player_data_cache:
            self.prepare_player_data(player_name)
        
        player_data = self.player_data_cache[player_name]
        gps_data = player_data['gps_data']
        
        if len(gps_data) == 0:
            return pd.DataFrame()
        
        # Get recent cycle data
        cycle_summary = gps_data[['date', 'J_minus', 'event_type']].copy()
        
        # Add physical load
        if 'Total Player Load' in gps_data.columns:
            cycle_summary['player_load'] = gps_data['Total Player Load']
        elif 'player_load' in gps_data.columns:
            cycle_summary['player_load'] = gps_data['player_load']
        else:
            cycle_summary['player_load'] = 0
        
        # Filter to recent cycle (last 15 days)
        cycle_summary = cycle_summary.tail(15)
        
        return cycle_summary


def main():
    """Example usage of the Cycle-to-Peak Predictor"""
    print("=" * 60)
    print("Cycle-to-Peak Performance Predictor")
    print("=" * 60)
    
    # Initialize predictor
    predictor = CycleToPeakPredictor()
    
    # Load data
    predictor.load_all_data()
    
    # Get list of available players
    if predictor.data_loader.gps_data is not None:
        available_players = predictor.data_loader.gps_data['name'].unique()[:5]  # First 5 players
        print(f"\nAvailable players: {list(available_players)}")
        
        # Process first player as example
        if len(available_players) > 0:
            player_name = available_players[0]
            print(f"\nProcessing player: {player_name}")
            
            # Prepare data
            player_data = predictor.prepare_player_data(player_name, position='midfielder')
            
            if len(player_data) > 0:
                # Train model
                print("\nTraining prediction model...")
                history = predictor.train_model(player_name)
                
                # Predict next match
                print("\nPredicting next match performance...")
                prediction = predictor.predict_next_match(player_name)
                
                print("\n" + "=" * 60)
                print("PREDICTION RESULTS")
                print("=" * 60)
                print(f"Player: {prediction['player_name']}")
                print(f"Match Readiness Score: {prediction['match_readiness_score']}/10")
                print(f"Days Until Match: {prediction['days_until_match']}")
                print(f"Recent Training Load: {prediction['recent_training_load']}")
                
                # Get performance evolution
                evolution = predictor.get_performance_evolution(player_name)
                if len(evolution) > 0:
                    print(f"\nHistorical Performance Ratings:")
                    print(evolution[['date', 'performance_rating']].tail(5).to_string(index=False))
                
                # Get training cycle
                cycle = predictor.get_training_cycle_summary(player_name)
                if len(cycle) > 0:
                    print(f"\nRecent Training Cycle (Last 15 days):")
                    print(cycle[['date', 'J_minus', 'event_type', 'player_load']].to_string(index=False))
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

