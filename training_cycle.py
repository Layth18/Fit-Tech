"""
Training Cycle Calculation Module
Calculates J- days (days until next match) for each training session
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class TrainingCycleCalculator:
    """Calculates training cycles and J- days for players"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.match_dates = None
        
    def identify_event_types(self, player_name: str, team_name: Optional[str] = None) -> pd.DataFrame:
        """
        Classify each day as 'Match Day', 'Training Day', or 'Rest Day'
        Returns a DataFrame with date, event_type, and J- (days until next match)
        """
        # Get player GPS data
        player_gps = self.data_loader.get_player_gps_data(player_name)
        
        if len(player_gps) == 0:
            print(f"No GPS data found for player: {player_name}")
            return pd.DataFrame()
        
        # Get match dates for the team
        if team_name:
            match_dates = self.data_loader.get_match_dates(team_name)
        else:
            # Try to infer team from GPS data
            if 'team_name' in player_gps.columns:
                team_name = player_gps['team_name'].iloc[0]
                match_dates = self.data_loader.get_match_dates(team_name)
            else:
                # Get all match dates
                match_dates = self.data_loader.get_match_dates()
        
        if len(match_dates) == 0:
            print("No match dates found")
            return pd.DataFrame()
        
        # Create a date range for all player activity
        min_date = player_gps['date'].min()
        max_date = player_gps['date'].max()
        
        # Get all unique dates from GPS data
        all_dates = pd.DataFrame({
            'date': pd.date_range(start=min_date, end=max_date, freq='D')
        })
        
        # Mark match days
        match_dates_list = match_dates['date'].unique()
        all_dates['is_match_day'] = all_dates['date'].isin(match_dates_list)
        
        # Calculate J- (days until next match) for each date
        all_dates['J_minus'] = all_dates['date'].apply(
            lambda d: self._calculate_j_minus(d, match_dates_list)
        )
        
        # Classify event type
        all_dates['event_type'] = all_dates.apply(
            lambda row: 'Match Day' if row['is_match_day'] 
            else ('Training Day' if row['J_minus'] is not None and row['J_minus'] > 0 
                  else 'Rest Day'),
            axis=1
        )
        
        # Merge with GPS data to get actual training sessions
        player_gps_with_cycle = player_gps.merge(
            all_dates[['date', 'event_type', 'J_minus']],
            on='date',
            how='left'
        )
        
        # For dates with GPS data but no match, classify as Training Day
        player_gps_with_cycle['event_type'] = player_gps_with_cycle['event_type'].fillna('Training Day')
        
        # Calculate J_minus for training days
        player_gps_with_cycle['J_minus'] = player_gps_with_cycle.apply(
            lambda row: self._calculate_j_minus(row['date'], match_dates_list) 
            if pd.isna(row['J_minus']) else row['J_minus'],
            axis=1
        )
        
        return player_gps_with_cycle
    
    def _calculate_j_minus(self, date: pd.Timestamp, match_dates: np.ndarray) -> Optional[int]:
        """Calculate days until next match (J-)"""
        # Find next match date
        future_matches = match_dates[match_dates > date]
        
        if len(future_matches) == 0:
            return None  # No future matches
        
        next_match = future_matches.min()
        days_until = (next_match - date).days
        
        return days_until if days_until > 0 else None
    
    def get_training_cycle_features(self, player_name: str, team_name: Optional[str] = None) -> pd.DataFrame:
        """
        Get training cycle features for a player
        Returns DataFrame with J_minus, physical load metrics, and cycle context
        """
        cycle_data = self.identify_event_types(player_name, team_name)
        
        if len(cycle_data) == 0:
            return pd.DataFrame()
        
        # Add cycle features
        cycle_data['cycle_id'] = cycle_data.apply(
            lambda row: self._get_cycle_id(row['date'], row['J_minus']),
            axis=1
        )
        
        # Calculate cycle position (where in the cycle)
        cycle_data['cycle_position'] = cycle_data.groupby('cycle_id')['J_minus'].transform(
            lambda x: (x.max() - x) / (x.max() - x.min() + 1) if x.max() != x.min() else 0.5
        )
        
        return cycle_data
    
    def _get_cycle_id(self, date: pd.Timestamp, j_minus: Optional[int]) -> int:
        """Assign a cycle ID based on match proximity"""
        if j_minus is None or pd.isna(j_minus):
            return -1
        
        # Simple cycle ID: based on the match date this cycle leads to
        # This is a simplified version - in production, you'd track actual match IDs
        try:
            return int(j_minus // 7)  # Rough cycle ID based on weeks
        except (ValueError, TypeError):
            return -1

