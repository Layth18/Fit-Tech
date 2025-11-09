"""
Advanced Feature Engineering Module
Creates features from GPS and Wyscout data for model training
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class FeatureEngineer:
    """Engineers features from physical and technical data"""
    
    def __init__(self):
        self.position_features = {
            'defender': ['defense_duels_defensifs_gagnes', 'defense_interceptions_total', 
                        'defense_duels_aeriens_gagnes', 'general_passes_precises'],
            'midfielder': ['general_passes_precises', 'general_passes_longues_precises',
                          'attack_passes_decisives', 'general_duels_gagnes'],
            'forward': ['attack_buts', 'attack_tirs_cadres', 'attack_xg', 
                       'attack_dribbles_reussis', 'attack_duels_offensifs_gagnes']
        }
    
    def extract_physical_features(self, gps_data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract physical performance features from GPS data
        """
        features = pd.DataFrame()
        
        # Volume Metrics
        if 'Total Distance (m)' in gps_data.columns:
            features['total_distance'] = gps_data['Total Distance (m)']
        else:
            features['total_distance'] = 0
        
        # Intensity Metrics
        if 'HS Distance (m)' in gps_data.columns:
            features['high_speed_distance'] = gps_data['HS Distance (m)']  # >19.8 km/h
        else:
            features['high_speed_distance'] = 0
        
        if 'Sprint' in gps_data.columns:
            features['sprint_distance'] = gps_data['Sprint']  # >25.2 km/h
        else:
            features['sprint_distance'] = 0
        
        if 'Total Player Load' in gps_data.columns:
            features['player_load'] = gps_data['Total Player Load']
        else:
            features['player_load'] = 0
        
        # Explosiveness Metrics
        if 'Accel + Decel Efforts' in gps_data.columns:
            features['accel_decel_efforts'] = gps_data['Accel + Decel Efforts']
        else:
            features['accel_decel_efforts'] = 0
        
        # Heart Rate Metrics
        if 'Avg HR (% Max)' in gps_data.columns:
            features['avg_hr_pct'] = gps_data['Avg HR (% Max)']
        else:
            features['avg_hr_pct'] = 0
        
        # Metabolic Power
        if 'High Metabolic Power Efforts' in gps_data.columns:
            features['high_metabolic_efforts'] = gps_data['High Metabolic Power Efforts']
        else:
            features['high_metabolic_efforts'] = 0
        
        # Duration
        if 'Total Duration' in gps_data.columns:
            features['duration'] = gps_data['Total Duration']
        else:
            features['duration'] = 0
        
        # Normalize by duration if available
        if 'duration' in features.columns:
            # Convert to numeric, handling mixed types
            duration_series = pd.to_numeric(features['duration'], errors='coerce')
            features['duration'] = duration_series.fillna(0)
            if features['duration'].sum() > 0:
                features['distance_per_min'] = features['total_distance'] / (features['duration'] / 60 + 1)
                features['player_load_per_min'] = features['player_load'] / (features['duration'] / 60 + 1)
            else:
                features['distance_per_min'] = 0
                features['player_load_per_min'] = 0
        else:
            features['distance_per_min'] = 0
            features['player_load_per_min'] = 0
        
        return features
    
    def extract_technical_features(self, player_match_data: pd.DataFrame, position: str = 'midfielder') -> pd.DataFrame:
        """
        Extract position-specific technical features from Wyscout data
        """
        features = pd.DataFrame()
        
        if len(player_match_data) == 0:
            return features
        
        # Position-specific features
        position_key = position.lower() if position.lower() in self.position_features else 'midfielder'
        key_metrics = self.position_features[position_key]
        
        # Extract available metrics
        for metric in key_metrics:
            if metric in player_match_data.columns:
                features[metric] = player_match_data[metric]
            else:
                features[metric] = 0
        
        # General metrics available for all positions
        general_metrics = {
            'general_passes_precises': 'pass_accuracy',
            'general_passes_total': 'passes_total',
            'general_duels_gagnes': 'duels_won',
            'general_duels_total': 'duels_total',
            'general_buts': 'goals',
            'attack_tirs_total': 'shots',
            'attack_tirs_cadres': 'shots_on_target'
        }
        
        for wyscout_col, feature_name in general_metrics.items():
            if wyscout_col in player_match_data.columns:
                features[feature_name] = player_match_data[wyscout_col]
            else:
                features[feature_name] = 0
        
        # Calculate percentages
        if 'passes_total' in features.columns and features['passes_total'].sum() > 0:
            features['pass_accuracy_pct'] = (features['pass_accuracy'] / 
                                            (features['passes_total'] + 1) * 100)
        else:
            features['pass_accuracy_pct'] = 0
        
        if 'duels_total' in features.columns and features['duels_total'].sum() > 0:
            features['duel_win_pct'] = (features['duels_won'] / 
                                       (features['duels_total'] + 1) * 100)
        else:
            features['duel_win_pct'] = 0
        
        return features
    
    def create_time_series_features(self, data: pd.DataFrame, date_col: str = 'date', 
                                   value_cols: List[str] = None) -> pd.DataFrame:
        """
        Create time-series features (rolling averages, trends, etc.)
        """
        if value_cols is None:
            value_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        data = data.sort_values(date_col)
        features = data.copy()
        
        # Rolling averages (5-match window)
        for col in value_cols:
            if col in data.columns:
                features[f'{col}_rolling_5'] = data[col].rolling(window=5, min_periods=1).mean()
                features[f'{col}_rolling_3'] = data[col].rolling(window=3, min_periods=1).mean()
                
                # Trend (difference from rolling average)
                features[f'{col}_trend'] = data[col] - features[f'{col}_rolling_5']
        
        return features
    
    def combine_features(self, physical_features: pd.DataFrame, 
                        technical_features: pd.DataFrame,
                        cycle_features: pd.DataFrame) -> pd.DataFrame:
        """
        Combine all feature sets into a single DataFrame
        """
        # Reset indices for alignment
        physical_features = physical_features.reset_index(drop=True)
        technical_features = technical_features.reset_index(drop=True)
        cycle_features = cycle_features.reset_index(drop=True)
        
        # Combine features
        combined = pd.concat([
            physical_features,
            technical_features,
            cycle_features[['J_minus', 'cycle_id', 'cycle_position', 'event_type']] if len(cycle_features) > 0 else pd.DataFrame()
        ], axis=1)
        
        # Fill NaN values
        combined = combined.fillna(0)
        
        return combined

