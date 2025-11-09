# GPS & Wyscout Sports Analytics ETL Pipeline - Database Summary

## Overview
This document summarizes the data tables created and populated based on the GPS & Wyscout Sports Analytics ETL Pipeline Documentation.

## Database File
- **Database**: `football_dw.db` (SQLite)

## Tables Created

### Dimension Tables

#### 1. dim_date
- **Purpose**: Date dimension table for time-based analysis
- **Columns**: 10
- **Records**: 2,557 (dates from 2020-01-01 to 2026-12-31)
- **Key Fields**: 
  - full_date, year, month, day, week, quarter, season, day_of_week, is_weekend

#### 2. dim_competition
- **Purpose**: Competition/League dimension
- **Columns**: 4
- **Records**: 8
- **Key Fields**: 
  - competition_id, competition_name, country, competition_type

#### 3. dim_team
- **Purpose**: Team dimension with GPS and Wyscout name mappings
- **Columns**: 6
- **Records**: 53
- **Key Fields**: 
  - team_id, team_name_std, team_name_gps, team_name_wyscout, has_gps, has_wyscout

#### 4. dim_player
- **Purpose**: Player dimension with GPS and Wyscout name mappings
- **Columns**: 6
- **Records**: 33
- **Key Fields**: 
  - player_id, player_name_std, player_name_gps, player_name_wyscout, has_gps, has_wyscout

#### 5. dim_match
- **Purpose**: Match dimension
- **Columns**: 9
- **Records**: 0 (to be populated)
- **Key Fields**: 
  - match_id, match_date, home_team_id, away_team_id, competition_id, home_score, away_score, match_type, opponent

### Fact Tables

#### 6. fact_player_gps
- **Purpose**: GPS tracking data for players
- **Columns**: 20
- **Records**: 2,108
- **Key Fields**: 
  - player_id, team_id, match_id, date_id, session_type, report_type, type_session, gameweek, opponent
  - total_distance_m, top_speed_kmh, accelerations, decelerations, average_speed_kmh
  - max_acceleration, max_deceleration, player_load_total, heart_rate_avg, heart_rate_max

#### 7. fact_player_wyscout
- **Purpose**: Wyscout player performance data
- **Columns**: 17
- **Records**: 0 (to be populated from player-specific CSV files)
- **Key Fields**: 
  - player_id, team_id, match_id, date_id, competition_id
  - minutes_played, goals, assists, xg, passes_total, passes_completed, passes_accuracy_pct
  - shots_total, shots_on_target, duels_won, duels_total

#### 8. fact_wyscout_match
- **Purpose**: Wyscout team match statistics
- **Columns**: 18
- **Records**: 9,222
- **Key Fields**: 
  - team_id, opponent_team_id, match_id, date_id, competition_id
  - formation, possession_pct, shots_total, shots_on_target, xg
  - passes_total, passes_completed, passes_accuracy_pct, duels_won, duels_total
  - goals_scored, goals_conceded

## Data Sources

### GPS Data
- **File**: `hackathon/Data After Extraction/CSV/matchs_gps.csv`
- **Records Processed**: 2,108
- **Contains**: Player GPS tracking metrics including distance, speed, acceleration, heart rate, etc.

### Wyscout Data
- **File**: `hackathon/Data After Extraction/CSV/wyscout_matchs.csv`
- **Records Processed**: 9,222
- **Contains**: Team match statistics including possession, shots, passes, duels, goals, etc.

## Scripts Created

1. **create_tables_simple.py**: Creates database schema and populates dimension tables
   - Uses only standard library (no external dependencies)
   - Creates all dimension and fact tables
   - Populates dim_date, dim_team, dim_competition, dim_player

2. **populate_fact_tables.py**: Populates fact tables from CSV files
   - Reads GPS and Wyscout CSV files
   - Maps data to dimension tables using lookups
   - Populates fact_player_gps and fact_wyscout_match

## Usage

### To create tables and populate dimension data:
```bash
python create_tables_simple.py
```

### To populate fact tables:
```bash
python populate_fact_tables.py
```

## Database Schema

The database follows a star schema design:
- **Dimension Tables**: Provide descriptive attributes (date, team, player, competition, match)
- **Fact Tables**: Store measurable events and metrics (GPS data, Wyscout statistics)

## Relationships

- `fact_player_gps` → `dim_player`, `dim_team`, `dim_match`, `dim_date`
- `fact_player_wyscout` → `dim_player`, `dim_team`, `dim_match`, `dim_date`, `dim_competition`
- `fact_wyscout_match` → `dim_team`, `dim_match`, `dim_date`, `dim_competition`
- `dim_match` → `dim_team`, `dim_competition`

## Next Steps

1. Populate `fact_player_wyscout` from player-specific CSV files
2. Populate `dim_match` from match data
3. Create additional indexes for performance
4. Add data validation and quality checks
5. Create views for common queries

## Notes

- All tables use foreign key constraints for data integrity
- Date dimension is pre-populated for years 2020-2026
- Team and player names are matched between GPS and Wyscout sources
- Some fact tables may have NULL values for optional fields

