"""
Performance Rating System
Creates composite Match Performance Rating using PCA-weighted metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

try:
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: scikit-learn not available. Using simplified rating calculation.")


class PerformanceRatingCalculator:
    """Calculates historical performance ratings for players"""
    
    def __init__(self, position: str = 'midfielder'):
        self.position = position
        if SKLEARN_AVAILABLE:
            self.scaler = StandardScaler()
            self.pca = PCA(n_components=0.95)  # Keep 95% of variance
        else:
            self.scaler = None
            self.pca = None
        self.feature_weights = None
        self.position_means = {}
        self.position_stds = {}
        
    def calculate_match_rating(self, physical_features: pd.DataFrame,
                              technical_features: pd.DataFrame,
                              position: str = None) -> pd.Series:
        """
        Calculate Match Performance Rating (1-10 scale) for each match
        Uses PCA-weighted combination of standardized metrics
        """
        if position:
            self.position = position
        
        # Combine features
        all_features = pd.concat([physical_features, technical_features], axis=1)
        
        # Select relevant features based on position
        feature_cols = self._get_position_features()
        available_cols = [col for col in feature_cols if col in all_features.columns]
        
        if len(available_cols) == 0:
            # Fallback: use all numeric columns
            available_cols = all_features.select_dtypes(include=[np.number]).columns.tolist()
        
        feature_data = all_features[available_cols].copy()
        
        # Standardize features (Z-scores)
        if SKLEARN_AVAILABLE and self.scaler is not None:
            feature_data_scaled = self.scaler.fit_transform(feature_data)
            feature_data_scaled = pd.DataFrame(feature_data_scaled, columns=available_cols)
        else:
            # Manual standardization
            feature_data_scaled = (feature_data - feature_data.mean()) / (feature_data.std() + 1e-6)
            feature_data_scaled = pd.DataFrame(feature_data_scaled, columns=available_cols)
        
        # Calculate position averages for comparison
        position_means = feature_data_scaled.mean()
        position_stds = feature_data_scaled.std()
        
        # Store for later use
        self.position_means = position_means.to_dict()
        self.position_stds = position_stds.to_dict()
        
        # Apply PCA to determine feature importance
        if SKLEARN_AVAILABLE and self.pca is not None:
            pca_features = self.pca.fit_transform(feature_data_scaled)
            use_pca = self.pca.n_components_ > 0
        else:
            pca_features = None
            use_pca = False
        
        # Calculate weighted score using first principal component
        # This captures the most variance in performance
        if use_pca:
            # Use first component as primary score
            primary_score = pca_features[:, 0]
            
            # Normalize to 1-10 scale
            min_score = primary_score.min()
            max_score = primary_score.max()
            
            if max_score > min_score:
                normalized_score = 1 + 9 * (primary_score - min_score) / (max_score - min_score)
            else:
                normalized_score = np.full(len(primary_score), 5.0)  # Default to middle
            
            # Alternative: weighted average of top features
            # Get feature loadings from PCA
            if SKLEARN_AVAILABLE and self.pca is not None:
                feature_loadings = self.pca.components_[0]
                feature_importance = np.abs(feature_loadings)
            else:
                # Equal weights if no PCA
                feature_importance = np.ones(len(available_cols)) / len(available_cols)
            
            # Weighted average of standardized features
            weighted_scores = []
            for idx in range(len(feature_data_scaled)):
                row = feature_data_scaled.iloc[idx].values
                weighted_score = np.sum(row * feature_importance)
                weighted_scores.append(weighted_score)
            
            weighted_scores = np.array(weighted_scores)
            
            # Normalize weighted scores to 1-10
            min_w = weighted_scores.min()
            max_w = weighted_scores.max()
            
            if max_w > min_w:
                normalized_weighted = 1 + 9 * (weighted_scores - min_w) / (max_w - min_w)
            else:
                normalized_weighted = np.full(len(weighted_scores), 5.0)
            
            # Combine both approaches (average)
            final_rating = (normalized_score + normalized_weighted) / 2
            
            self.feature_weights = dict(zip(available_cols, feature_importance))
            
        else:
            # Fallback: simple average of standardized features
            final_rating = feature_data_scaled.mean(axis=1)
            final_rating = 1 + 9 * (final_rating - final_rating.min()) / (final_rating.max() - final_rating.min() + 1e-6)
        
        return pd.Series(final_rating, name='performance_rating')
    
    def _get_position_features(self) -> List[str]:
        """Get relevant features for the player's position"""
        position_features = {
            'defender': [
                'defense_duels_defensifs_gagnes', 'defense_interceptions_total',
                'defense_duels_aeriens_gagnes', 'general_passes_precises',
                'player_load', 'total_distance', 'high_speed_distance'
            ],
            'midfielder': [
                'general_passes_precises', 'general_passes_longues_precises',
                'attack_passes_decisives', 'general_duels_gagnes',
                'player_load', 'total_distance', 'accel_decel_efforts'
            ],
            'forward': [
                'attack_buts', 'attack_tirs_cadres', 'attack_xg',
                'attack_dribbles_reussis', 'attack_duels_offensifs_gagnes',
                'sprint_distance', 'high_speed_distance', 'player_load'
            ]
        }
        
        return position_features.get(self.position.lower(), position_features['midfielder'])
    
    def get_rating_with_context(self, rating: pd.Series, 
                                match_data: pd.DataFrame) -> pd.DataFrame:
        """
        Add context to performance ratings (date, opponent, etc.)
        """
        result = pd.DataFrame({
            'date': match_data['date'].values if 'date' in match_data.columns else range(len(rating)),
            'performance_rating': rating.values,
            'match': match_data['match'].values if 'match' in match_data.columns else ['Unknown'] * len(rating),
            'opponent': match_data.get('adversaire', ['Unknown'] * len(rating))
        })
        
        return result

