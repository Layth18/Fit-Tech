"""
Script to create data tables and populate them from CSV files.
Based on GPS & Wyscout Sports Analytics ETL Pipeline Documentation.
"""

# Import pandas with error handling (required dependency)
try:
    import pandas as pd  # type: ignore
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None  # type: ignore
    print("✗ Error: pandas package is required but not installed.")
    print("  Install it with: pip install pandas")

# Import sqlalchemy with error handling (required dependency)
try:
    from sqlalchemy import create_engine, text, inspect  # type: ignore
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    create_engine = None  # type: ignore
    text = None  # type: ignore
    inspect = None  # type: ignore
    print("✗ Error: sqlalchemy package is required but not installed.")
    print("  Install it with: pip install sqlalchemy")

# Import rapidfuzz with error handling (optional dependency)
try:
    from rapidfuzz import process, fuzz  # type: ignore
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False
    process = None  # type: ignore
    fuzz = None  # type: ignore
    print("⚠ Warning: rapidfuzz package not installed. Install it with: pip install rapidfuzz")
    print("  Team name matching will use simple string matching instead.")

import os
from datetime import date as date_type
import sqlite3

# File paths
DB_PATH = "football_dw.db"
GPS_MATCHES_CSV = "hackathon/Data After Extraction/CSV/matchs_gps.csv"
GPS_TRAINING_CSV = "hackathon/Data After Extraction/CSV/training_gps.csv"
WYSCOUT_MATCHES_CSV = "hackathon/Data After Extraction/CSV/wyscout_matchs.csv"
WYSCOUT_PLAYERS_OUTFIELD_CSV = "hackathon/Data After Extraction/CSV/wyscout_players_outfield.csv"
WYSCOUT_PLAYERS_GOALKEEPER_CSV = "hackathon/Data After Extraction/CSV/wyscout_players_goalkeeper.csv"

# Create database engine (only if sqlalchemy is available)
if SQLALCHEMY_AVAILABLE:
    engine = create_engine(f"sqlite:///{DB_PATH}")
else:
    engine = None

def create_comprehensive_schema():
    """Create comprehensive database schema."""
    if not SQLALCHEMY_AVAILABLE or engine is None:
        print("✗ Cannot create schema: sqlalchemy is not available")
        return False
    
    print("=" * 80)
    print("CREATING DATABASE SCHEMA")
    print("=" * 80)
    
    schema_sql = """
-- ============================================
-- DIMENSION TABLES
-- ============================================

-- DIM_DATE - Date dimension table
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    week INTEGER,
    quarter INTEGER,
    season VARCHAR(20),
    day_of_week VARCHAR(20),
    is_weekend BOOLEAN
);

-- DIM_COMPETITION - Competition/League dimension
CREATE TABLE IF NOT EXISTS dim_competition (
    competition_id INTEGER PRIMARY KEY,
    competition_name VARCHAR(200) UNIQUE NOT NULL,
    country VARCHAR(100),
    competition_type VARCHAR(50)
);

-- DIM_TEAM - Team dimension
CREATE TABLE IF NOT EXISTS dim_team (
    team_id INTEGER PRIMARY KEY,
    team_name_std VARCHAR(200),
    team_name_gps VARCHAR(200),
    team_name_wyscout VARCHAR(200),
    has_gps BOOLEAN DEFAULT 0,
    has_wyscout BOOLEAN DEFAULT 0
);

-- DIM_PLAYER - Player dimension
CREATE TABLE IF NOT EXISTS dim_player (
    player_id INTEGER PRIMARY KEY,
    player_name_std VARCHAR(200),
    player_name_gps VARCHAR(200),
    player_name_wyscout VARCHAR(200),
    has_gps BOOLEAN DEFAULT 0,
    has_wyscout BOOLEAN DEFAULT 0
);

-- DIM_MATCH - Match dimension
CREATE TABLE IF NOT EXISTS dim_match (
    match_id INTEGER PRIMARY KEY,
    match_date DATE,
    home_team_id INTEGER,
    away_team_id INTEGER,
    competition_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    match_type VARCHAR(50),
    opponent VARCHAR(200),
    FOREIGN KEY (home_team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (competition_id) REFERENCES dim_competition(competition_id)
);

-- ============================================
-- FACT TABLES
-- ============================================

-- FACT_PLAYER_GPS - GPS tracking data for players
CREATE TABLE IF NOT EXISTS fact_player_gps (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    team_id INTEGER,
    match_id INTEGER,
    date_id INTEGER,
    session_type VARCHAR(50),
    report_type VARCHAR(100),
    type_session VARCHAR(50),
    gameweek VARCHAR(50),
    opponent VARCHAR(200),
    total_distance_m REAL,
    top_speed_kmh REAL,
    accelerations INTEGER,
    decelerations INTEGER,
    average_speed_kmh REAL,
    max_acceleration REAL,
    max_deceleration REAL,
    player_load_total REAL,
    heart_rate_avg REAL,
    heart_rate_max REAL,
    FOREIGN KEY (player_id) REFERENCES dim_player(player_id),
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (match_id) REFERENCES dim_match(match_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

-- FACT_PLAYER_WYSCOUT - Wyscout player performance data
CREATE TABLE IF NOT EXISTS fact_player_wyscout (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    team_id INTEGER,
    match_id INTEGER,
    date_id INTEGER,
    competition_id INTEGER,
    minutes_played INTEGER,
    goals INTEGER,
    assists INTEGER,
    xg REAL,
    passes_total INTEGER,
    passes_completed INTEGER,
    passes_accuracy_pct REAL,
    shots_total INTEGER,
    shots_on_target INTEGER,
    duels_won INTEGER,
    duels_total INTEGER,
    FOREIGN KEY (player_id) REFERENCES dim_player(player_id),
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (match_id) REFERENCES dim_match(match_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (competition_id) REFERENCES dim_competition(competition_id)
);

-- FACT_WYSCOUT_MATCH - Wyscout team match statistics
CREATE TABLE IF NOT EXISTS fact_wyscout_match (
    id INTEGER PRIMARY KEY,
    team_id INTEGER,
    opponent_team_id INTEGER,
    match_id INTEGER,
    date_id INTEGER,
    competition_id INTEGER,
    formation VARCHAR(50),
    possession_pct REAL,
    shots_total INTEGER,
    shots_on_target INTEGER,
    xg REAL,
    passes_total INTEGER,
    passes_completed INTEGER,
    passes_accuracy_pct REAL,
    duels_won INTEGER,
    duels_total INTEGER,
    goals_scored INTEGER,
    goals_conceded INTEGER,
    FOREIGN KEY (team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (opponent_team_id) REFERENCES dim_team(team_id),
    FOREIGN KEY (match_id) REFERENCES dim_match(match_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (competition_id) REFERENCES dim_competition(competition_id)
);
"""
    
    with engine.begin() as conn:
        for statement in schema_sql.split(";"):
            stmt = statement.strip()
            if stmt:
                try:
                    conn.execute(text(stmt))
                    table_name = stmt.split()[5] if "CREATE TABLE" in stmt else None
                    if table_name:
                        print(f"✓ Created table: {table_name}")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"⚠ Warning: {e}")
    
    print("\n✓ Database schema created successfully!")
    return True

def populate_dim_date():
    """Populate the date dimension table."""
    if not PANDAS_AVAILABLE or not SQLALCHEMY_AVAILABLE or engine is None:
        print("✗ Cannot populate dim_date: required packages not available")
        return
    
    print("\n" + "=" * 80)
    print("POPULATING DIM_DATE")
    print("=" * 80)
    
    try:
        # Check if already populated
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_date"))
            count = result.scalar()
            if count > 0:
                print(f"✓ dim_date already populated with {count} records")
                return
    except:
        pass
    
    start_date = date_type(2020, 1, 1)
    end_date = date_type(2026, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    
    dim_date = pd.DataFrame({
        "full_date": dates.date,
        "year": dates.year,
        "month": dates.month,
        "day": dates.day,
        "week": dates.isocalendar().week,
        "quarter": dates.quarter,
        "season": [f"{y}-{y+1}" if m >= 7 else f"{y-1}-{y}" for y, m in zip(dates.year, dates.month)],
        "day_of_week": dates.day_name(),
        "is_weekend": dates.weekday >= 5
    })
    
    try:
        dim_date.to_sql("dim_date", engine, if_exists="append", index=False, method="multi")
        print(f"✓ Populated dim_date with {len(dim_date)} records")
    except Exception as e:
        if "UNIQUE constraint" in str(e):
            print(f"✓ dim_date already populated")
        else:
            print(f"⚠ Error populating dim_date: {e}")

def populate_dim_tables_from_csv():
    """Populate dimension tables from CSV files."""
    print("\n" + "=" * 80)
    print("POPULATING DIMENSION TABLES FROM CSV FILES")
    print("=" * 80)
    
    # Read CSV files
    if not os.path.exists(GPS_MATCHES_CSV):
        print(f"⚠ GPS CSV file not found: {GPS_MATCHES_CSV}")
        return
    
    if not os.path.exists(WYSCOUT_MATCHES_CSV):
        print(f"⚠ Wyscout CSV file not found: {WYSCOUT_MATCHES_CSV}")
        return
    
    # Read GPS data
    print(f"\nReading GPS data from {GPS_MATCHES_CSV}...")
    try:
        gps_df = pd.read_csv(GPS_MATCHES_CSV, low_memory=False, nrows=1000)  # Read sample first
        print(f"✓ Loaded {len(gps_df)} GPS records (sample)")
    except Exception as e:
        print(f"⚠ Error reading GPS CSV: {e}")
        return
    
    # Read Wyscout data
    print(f"Reading Wyscout data from {WYSCOUT_MATCHES_CSV}...")
    try:
        wyscout_df = pd.read_csv(WYSCOUT_MATCHES_CSV, low_memory=False, nrows=1000)  # Read sample first
        print(f"✓ Loaded {len(wyscout_df)} Wyscout records (sample)")
    except Exception as e:
        print(f"⚠ Error reading Wyscout CSV: {e}")
        return
    
    # Populate dim_team
    print("\n--- Populating dim_team ---")
    teams_gps = gps_df["team_name"].dropna().unique() if "team_name" in gps_df.columns else []
    teams_wyscout = wyscout_df["equipe"].dropna().unique() if "equipe" in wyscout_df.columns else []
    
    # Get existing teams from database
    try:
        existing_teams = pd.read_sql("SELECT team_name_std FROM dim_team", engine)["team_name_std"].tolist()
    except:
        existing_teams = []
    
    team_records = []
    processed_teams = set(existing_teams)
    
    # Process GPS teams
    for team_gps in teams_gps:
        if team_gps not in processed_teams:
            if RAPIDFUZZ_AVAILABLE and len(teams_wyscout) > 0:
                match = process.extractOne(team_gps, teams_wyscout, scorer=fuzz.token_set_ratio)
            else:
                # Simple string matching fallback
                match = None
                if len(teams_wyscout) > 0:
                    for team_wyscout in teams_wyscout:
                        if team_gps.lower() in team_wyscout.lower() or team_wyscout.lower() in team_gps.lower():
                            match = (team_wyscout, 80)  # Simulate match score
                            break
            if match and match[1] >= 80:
                team_records.append({
                    "team_name_std": team_gps,
                    "team_name_gps": team_gps,
                    "team_name_wyscout": match[0],
                    "has_gps": True,
                    "has_wyscout": True
                })
            else:
                team_records.append({
                    "team_name_std": team_gps,
                    "team_name_gps": team_gps,
                    "team_name_wyscout": None,
                    "has_gps": True,
                    "has_wyscout": False
                })
            processed_teams.add(team_gps)
    
    # Process Wyscout teams not in GPS
    for team_wyscout in teams_wyscout:
        if team_wyscout not in processed_teams:
            team_records.append({
                "team_name_std": team_wyscout,
                "team_name_gps": None,
                "team_name_wyscout": team_wyscout,
                "has_gps": False,
                "has_wyscout": True
            })
            processed_teams.add(team_wyscout)
    
    if team_records:
        dim_team_df = pd.DataFrame(team_records)
        try:
            dim_team_df.to_sql("dim_team", engine, if_exists="append", index=False)
            print(f"✓ Populated dim_team with {len(dim_team_df)} teams")
        except Exception as e:
            print(f"⚠ Error populating dim_team: {e}")
    else:
        print("✓ No new teams to add")
    
    # Populate dim_competition
    print("\n--- Populating dim_competition ---")
    if "competition" in wyscout_df.columns:
        competitions = wyscout_df["competition"].dropna().unique()
        
        # Get existing competitions
        try:
            existing_competitions = pd.read_sql("SELECT competition_name FROM dim_competition", engine)["competition_name"].tolist()
        except:
            existing_competitions = []
        
        competition_records = [{"competition_name": comp} for comp in competitions if comp not in existing_competitions]
        
        if competition_records:
            dim_competition_df = pd.DataFrame(competition_records)
            try:
                dim_competition_df.to_sql("dim_competition", engine, if_exists="append", index=False)
                print(f"✓ Populated dim_competition with {len(dim_competition_df)} competitions")
            except Exception as e:
                print(f"⚠ Error populating dim_competition: {e}")
        else:
            print("✓ No new competitions to add")
    
    # Populate dim_player
    print("\n--- Populating dim_player ---")
    players_gps = gps_df["name"].dropna().unique() if "name" in gps_df.columns else []
    
    # Get existing players
    try:
        existing_players = pd.read_sql("SELECT player_name_std FROM dim_player", engine)["player_name_std"].tolist()
    except:
        existing_players = []
    
    player_records = []
    for player_gps in players_gps:
        if player_gps not in existing_players:
            player_records.append({
                "player_name_std": player_gps,
                "player_name_gps": player_gps,
                "player_name_wyscout": None,
                "has_gps": True,
                "has_wyscout": False
            })
    
    if player_records:
        dim_player_df = pd.DataFrame(player_records)
        try:
            dim_player_df.to_sql("dim_player", engine, if_exists="append", index=False)
            print(f"✓ Populated dim_player with {len(dim_player_df)} players")
        except Exception as e:
            print(f"⚠ Error populating dim_player: {e}")
    else:
        print("✓ No new players to add")

def populate_fact_tables():
    """Populate fact tables from CSV files."""
    print("\n" + "=" * 80)
    print("POPULATING FACT TABLES FROM CSV FILES")
    print("=" * 80)
    
    # Read dimension tables for lookups
    try:
        dim_team = pd.read_sql("SELECT team_id, team_name_gps, team_name_wyscout FROM dim_team", engine)
        dim_player = pd.read_sql("SELECT player_id, player_name_gps FROM dim_player", engine)
        dim_competition = pd.read_sql("SELECT competition_id, competition_name FROM dim_competition", engine)
        dim_date = pd.read_sql("SELECT date_id, full_date FROM dim_date", engine)
    except Exception as e:
        print(f"⚠ Error reading dimension tables: {e}")
        return
    
    # Create lookup dictionaries
    team_lookup_gps = dict(zip(dim_team["team_name_gps"].dropna(), dim_team["team_id"]))
    team_lookup_wyscout = dict(zip(dim_team["team_name_wyscout"].dropna(), dim_team["team_id"]))
    player_lookup = dict(zip(dim_player["player_name_gps"].dropna(), dim_player["player_id"]))
    competition_lookup = dict(zip(dim_competition["competition_name"], dim_competition["competition_id"]))
    dim_date["full_date"] = pd.to_datetime(dim_date["full_date"]).dt.date
    date_lookup = dict(zip(dim_date["full_date"], dim_date["date_id"]))
    
    # Populate fact_player_gps
    print("\n--- Populating fact_player_gps ---")
    if os.path.exists(GPS_MATCHES_CSV):
        try:
            print(f"Reading {GPS_MATCHES_CSV}...")
            gps_df = pd.read_csv(GPS_MATCHES_CSV, low_memory=False)
            print(f"✓ Loaded {len(gps_df)} GPS records")
            
            # Map columns
            fact_gps_records = []
            for idx, row in gps_df.iterrows():
                if idx % 100 == 0:
                    print(f"  Processing record {idx}/{len(gps_df)}...")
                
                player_id = player_lookup.get(row.get("name"))
                team_id = team_lookup_gps.get(row.get("team_name"))
                
                # Parse date
                date_str = row.get("date")
                date_id = None
                if date_str:
                    try:
                        date_obj = pd.to_datetime(date_str).date()
                        date_id = date_lookup.get(date_obj)
                    except:
                        pass
                
                fact_gps_records.append({
                    "player_id": player_id,
                    "team_id": team_id,
                    "match_id": None,  # Will be populated later
                    "date_id": date_id,
                    "session_type": row.get("type_session"),
                    "report_type": row.get("report_type"),
                    "type_session": row.get("type_session"),
                    "gameweek": row.get("gameweek"),
                    "opponent": row.get("opponent"),
                    "total_distance_m": row.get("Total Distance (m)") if "Total Distance (m)" in row else None,
                    "top_speed_kmh": row.get("Maximum Velocity (km/h)") if "Maximum Velocity (km/h)" in row else None,
                    "accelerations": row.get("Acceleration B1 Efforts (Gen 2)") if "Acceleration B1 Efforts (Gen 2)" in row else None,
                    "decelerations": row.get("Deceleration B1 Efforts (Gen 2)") if "Deceleration B1 Efforts (Gen 2)" in row else None,
                    "average_speed_kmh": row.get("Average Velocity (km/h)") if "Average Velocity (km/h)" in row else None,
                    "max_acceleration": row.get("Max Acceleration") if "Max Acceleration" in row else None,
                    "max_deceleration": row.get("Max Deceleration") if "Max Deceleration" in row else None,
                    "player_load_total": row.get("Total Player Load") if "Total Player Load" in row else None,
                    "heart_rate_avg": row.get("Avg Heart Rate") if "Avg Heart Rate" in row else None,
                    "heart_rate_max": row.get("Maximum Heart Rate") if "Maximum Heart Rate" in row else None,
                })
            
            if fact_gps_records:
                fact_gps_df = pd.DataFrame(fact_gps_records)
                fact_gps_df.to_sql("fact_player_gps", engine, if_exists="append", index=False)
                print(f"✓ Populated fact_player_gps with {len(fact_gps_df)} records")
        except Exception as e:
            print(f"⚠ Error populating fact_player_gps: {e}")
            import traceback
            traceback.print_exc()
    
    # Populate fact_wyscout_match
    print("\n--- Populating fact_wyscout_match ---")
    if os.path.exists(WYSCOUT_MATCHES_CSV):
        try:
            print(f"Reading {WYSCOUT_MATCHES_CSV}...")
            wyscout_df = pd.read_csv(WYSCOUT_MATCHES_CSV, low_memory=False)
            print(f"✓ Loaded {len(wyscout_df)} Wyscout match records")
            
            fact_match_records = []
            for idx, row in wyscout_df.iterrows():
                if idx % 100 == 0:
                    print(f"  Processing record {idx}/{len(wyscout_df)}...")
                
                team_id = team_lookup_wyscout.get(row.get("equipe"))
                opponent_id = team_lookup_wyscout.get(row.get("adversaire"))
                competition_id = competition_lookup.get(row.get("competition"))
                
                # Parse date
                date_str = row.get("date")
                date_id = None
                if date_str:
                    try:
                        date_obj = pd.to_datetime(date_str).date()
                        date_id = date_lookup.get(date_obj)
                    except:
                        pass
                
                # Parse score
                score_str = row.get("score", "")
                goals_scored = None
                goals_conceded = None
                if score_str and ":" in str(score_str):
                    try:
                        parts = str(score_str).split(":")
                        if len(parts) == 2:
                            goals_scored = int(parts[0].strip())
                            goals_conceded = int(parts[1].strip())
                    except:
                        pass
                
                fact_match_records.append({
                    "team_id": team_id,
                    "opponent_team_id": opponent_id,
                    "match_id": None,  # Will be populated later
                    "date_id": date_id,
                    "competition_id": competition_id,
                    "formation": row.get("formation"),
                    "possession_pct": row.get("general_possession_pct"),
                    "shots_total": row.get("general_tirs_total"),
                    "shots_on_target": row.get("general_tirs_cadres"),
                    "xg": row.get("general_xg"),
                    "passes_total": row.get("general_passes_total"),
                    "passes_completed": row.get("general_passes_precises"),
                    "passes_accuracy_pct": row.get("general_passes_precises_pct"),
                    "duels_won": row.get("general_duels_gagnes"),
                    "duels_total": row.get("general_duels_total"),
                    "goals_scored": goals_scored,
                    "goals_conceded": goals_conceded,
                })
            
            if fact_match_records:
                fact_match_df = pd.DataFrame(fact_match_records)
                fact_match_df.to_sql("fact_wyscout_match", engine, if_exists="append", index=False)
                print(f"✓ Populated fact_wyscout_match with {len(fact_match_df)} records")
        except Exception as e:
            print(f"⚠ Error populating fact_wyscout_match: {e}")
            import traceback
            traceback.print_exc()

def display_database_summary():
    """Display summary of created database."""
    if not SQLALCHEMY_AVAILABLE or not PANDAS_AVAILABLE or engine is None:
        print("✗ Cannot display summary: required packages not available")
        return
    
    print("\n" + "=" * 80)
    print("DATABASE SUMMARY")
    print("=" * 80)
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n✓ Created {len(tables)} tables:")
        
        for table_name in tables:
            try:
                columns = inspector.get_columns(table_name)
                count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table_name}", engine)["cnt"].iloc[0]
                print(f"  - {table_name}: {len(columns)} columns, {count:,} records")
            except Exception as e:
                print(f"  - {table_name}: {len(columns)} columns (error reading count: {e})")
    except Exception as e:
        print(f"✗ Error displaying summary: {e}")

def main():
    """Main execution function."""
    print("=" * 80)
    print("GPS & WYSCOUT SPORTS ANALYTICS ETL PIPELINE")
    print("Table Creation and Data Population")
    print("=" * 80)
    
    # Step 1: Create database schema
    print("\n[Step 1] Creating database schema...")
    create_comprehensive_schema()
    
    # Step 2: Populate dimension tables
    print("\n[Step 2] Populating dimension tables...")
    populate_dim_date()
    populate_dim_tables_from_csv()
    
    # Step 3: Populate fact tables
    print("\n[Step 3] Populating fact tables...")
    populate_fact_tables()
    
    # Step 4: Display summary
    display_database_summary()
    
    print("\n" + "=" * 80)
    print("✓ PROCESS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\nDatabase file: {DB_PATH}")

if __name__ == "__main__":
    main()

