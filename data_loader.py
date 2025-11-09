"""
Data Loading and Preprocessing Module
Handles loading GPS and Wyscout data, and basic preprocessing
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class DataLoader:
    """Loads and preprocesses GPS and Wyscout data"""
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self.gps_data = None
        self.match_data = None
        self.player_data = None
        
    def load_gps_data(self, file_path: str = "training_gps.csv") -> pd.DataFrame:
        """Load GPS training data"""
        print(f"Loading GPS data from {file_path}...")
        self.gps_data = pd.read_csv(file_path)
        
        # Convert date column to datetime
        if 'date' in self.gps_data.columns:
            self.gps_data['date'] = pd.to_datetime(self.gps_data['date'])
        
        # Fill missing values with 0 for numeric columns
        numeric_cols = self.gps_data.select_dtypes(include=[np.number]).columns
        self.gps_data[numeric_cols] = self.gps_data[numeric_cols].fillna(0)
        
        print(f"Loaded {len(self.gps_data)} GPS records")
        return self.gps_data
    
    def load_match_data(self, file_path: str = "wyscout_matchs.csv") -> pd.DataFrame:
        """Load match-level Wyscout data"""
        print(f"Loading match data from {file_path}...")
        self.match_data = pd.read_csv(file_path)
        
        # Convert date column to datetime
        if 'date' in self.match_data.columns:
            self.match_data['date'] = pd.to_datetime(self.match_data['date'])
        
        print(f"Loaded {len(self.match_data)} match records")
        return self.match_data
    
    def load_player_data(self, file_path: str = "wyscout_players_outfield.csv") -> pd.DataFrame:
        """Load player-level Wyscout data"""
        print(f"Loading player data from {file_path}...")
        self.player_data = pd.read_csv(file_path)
        
        # Convert date column to datetime
        if 'date' in self.player_data.columns:
            self.player_data['date'] = pd.to_datetime(self.player_data['date'])
        
        # Fill missing values with 0 for numeric columns
        numeric_cols = self.player_data.select_dtypes(include=[np.number]).columns
        self.player_data[numeric_cols] = self.player_data[numeric_cols].fillna(0)
        
        print(f"Loaded {len(self.player_data)} player records")
        return self.player_data
    
    def get_player_gps_data(self, player_name: str) -> pd.DataFrame:
        """Get GPS data for a specific player"""
        if self.gps_data is None:
            raise ValueError("GPS data not loaded. Call load_gps_data() first.")
        
        player_gps = self.gps_data[self.gps_data['name'] == player_name].copy()
        player_gps = player_gps.sort_values('date')
        return player_gps
    
    def get_player_match_data(self, player_name: str) -> pd.DataFrame:
        """Get match data for a specific player"""
        if self.player_data is None:
            raise ValueError("Player data not loaded. Call load_player_data() first.")
        
        player_matches = self.player_data[self.player_data['player'] == player_name].copy()
        player_matches = player_matches.sort_values('date')
        return player_matches
    
    def get_match_dates(self, team_name: Optional[str] = None) -> pd.DataFrame:
        """Get all match dates, optionally filtered by team"""
        if self.match_data is None:
            raise ValueError("Match data not loaded. Call load_match_data() first.")
        
        match_dates = self.match_data[['date', 'team_name', 'match']].copy()
        match_dates = match_dates.drop_duplicates(subset=['date', 'team_name'])
        match_dates = match_dates.sort_values('date')
        
        if team_name:
            match_dates = match_dates[match_dates['team_name'] == team_name]
        
        return match_dates

