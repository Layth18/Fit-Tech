"""
GPS & Wyscout Sports Analytics ETL Pipeline
Complete database creation and population script
"""

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
    print("  The script cannot run without this package.")

# Import pandas with error handling (required dependency)
try:
    import pandas as pd  # type: ignore
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None  # type: ignore
    print("✗ Error: pandas package is required but not installed.")
    print("  Install it with: pip install pandas")
    print("  The script cannot run without this package.")

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

from datetime import date
import os

# Configuration
DB_PATH = "football_dw.db"
GPS_CSV_PATH = "hackathon/Data After Extraction/CSV/matchs_gps.csv"
WYSCOUT_CSV_PATH = "hackathon/Data After Extraction/CSV/wyscout_matchs.csv"

# Create database engine (only if sqlalchemy is available)
if SQLALCHEMY_AVAILABLE:
    engine = create_engine(f"sqlite:///{DB_PATH}")
else:
    engine = None

def test_connection():
    """Test database connection."""
    if not SQLALCHEMY_AVAILABLE or engine is None:
        print("✗ Cannot test connection: sqlalchemy is not available")
        return False
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✓ Connection OK:", result.scalar())
            return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def create_dimension_tables():
    """Create all dimension tables."""
    print("\n" + "=" * 80)
    print("CREATING DIMENSION TABLES")
    print("=" * 80)
    
    schema_sql = """
    -- DIM_DATE
    CREATE TABLE IF NOT EXISTS dim_date (
        date_id INTEGER PRIMARY KEY,
        full_date DATE UNIQUE NOT NULL,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        week INTEGER,
        quarter INTEGER,
        season VARCHAR(20)
    );

    -- DIM_COMPETITION
    CREATE TABLE IF NOT EXISTS dim_competition (
        competition_id INTEGER PRIMARY KEY,
        competition_name VARCHAR(100) UNIQUE NOT NULL
    );

    -- DIM_TEAM
    CREATE TABLE IF NOT EXISTS dim_team (
        team_id INTEGER PRIMARY KEY,
        team_name_std VARCHAR(100),
        team_name_gps VARCHAR(100),
        team_name_wyscout VARCHAR(100),
        has_gps BOOLEAN DEFAULT 0,
        has_wyscout BOOLEAN DEFAULT 0
    );

    -- DIM_PLAYER
    CREATE TABLE IF NOT EXISTS dim_player (
        player_id INTEGER PRIMARY KEY,
        player_name_std VARCHAR(100),
        player_name_gps VARCHAR(100),
        player_name_wyscout VARCHAR(100),
        has_gps BOOLEAN DEFAULT 0,
        has_wyscout BOOLEAN DEFAULT 0
    );

    -- DIM_MATCH
    CREATE TABLE IF NOT EXISTS dim_match (
        match_id INTEGER PRIMARY KEY,
        match_date DATE,
        home_team_id INTEGER,
        away_team_id INTEGER,
        competition_id INTEGER,
        FOREIGN KEY (home_team_id) REFERENCES dim_team(team_id),
        FOREIGN KEY (away_team_id) REFERENCES dim_team(team_id),
        FOREIGN KEY (competition_id) REFERENCES dim_competition(competition_id)
    );
    """
    
    try:
        with engine.begin() as conn:
            for statement in schema_sql.split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))
        print("✓ Dimension tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating dimension tables: {e}")
        return False

def populate_dim_date():
    """Populate the date dimension table."""
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
                return True
        
        start_date = date(2015, 9, 1)
        end_date = date(2026, 12, 31)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        
        dim_date_df = pd.DataFrame({
            "full_date": dates.date,
            "year": dates.year,
            "month": dates.month,
            "day": dates.day,
            "week": dates.isocalendar().week,
            "quarter": dates.quarter,
            "season": [f"{y}-{y+1}" if m >= 7 else f"{y-1}-{y}" for y, m in zip(dates.year, dates.month)]
        })
        
        try:
            dim_date_df.to_sql("dim_date", engine, if_exists="append", index=False)
            print(f"✓ Populated dim_date with {len(dim_date_df)} records")
            return True
        except Exception as e:
            if "UNIQUE constraint" in str(e) or "already exists" in str(e).lower():
                print(f"✓ dim_date already populated (some dates may already exist)")
                return True
            else:
                raise
    except Exception as e:
        print(f"✗ Error populating dim_date: {e}")
        import traceback
        traceback.print_exc()
        return False

def populate_dim_team():
    """Populate the team dimension table from CSV files."""
    print("\n" + "=" * 80)
    print("POPULATING DIM_TEAM")
    print("=" * 80)
    
    try:
        # Check if already populated
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_team"))
            count = result.scalar()
            if count > 0:
                print(f"✓ dim_team already populated with {count} records")
                return True
        
        # Read GPS data
        teams_gps = []
        if os.path.exists(GPS_CSV_PATH):
            try:
                gps_df = pd.read_csv(GPS_CSV_PATH, low_memory=False, nrows=1000)  # Sample first
                if "team_name" in gps_df.columns:
                    teams_gps = gps_df["team_name"].dropna().unique().tolist()
                print(f"  Found {len(teams_gps)} GPS teams")
            except Exception as e:
                print(f"  ⚠ Error reading GPS CSV: {e}")
        else:
            print(f"  ⚠ GPS CSV file not found: {GPS_CSV_PATH}")
        
        # Read Wyscout data
        teams_wyscout = []
        if os.path.exists(WYSCOUT_CSV_PATH):
            try:
                wyscout_df = pd.read_csv(WYSCOUT_CSV_PATH, low_memory=False, nrows=1000)  # Sample first
                if "equipe" in wyscout_df.columns:
                    teams_wyscout = wyscout_df["equipe"].dropna().unique().tolist()
                print(f"  Found {len(teams_wyscout)} Wyscout teams")
            except Exception as e:
                print(f"  ⚠ Error reading Wyscout CSV: {e}")
        else:
            print(f"  ⚠ Wyscout CSV file not found: {WYSCOUT_CSV_PATH}")
        
        # Match teams
        team_records = []
        matched_wyscout_teams = set()
        
        for team_gps in teams_gps:
            if len(teams_wyscout) > 0:
                if RAPIDFUZZ_AVAILABLE:
                    match = process.extractOne(team_gps, teams_wyscout, scorer=fuzz.token_set_ratio)
                    if match and match[1] >= 85:
                        team_records.append((team_gps, match[0], True, True))
                        matched_wyscout_teams.add(match[0])
                    else:
                        team_records.append((team_gps, None, True, False))
                else:
                    # Simple string matching fallback
                    match_found = None
                    for team_wyscout in teams_wyscout:
                        if team_gps.lower() in team_wyscout.lower() or team_wyscout.lower() in team_gps.lower():
                            match_found = team_wyscout
                            break
                    if match_found:
                        team_records.append((team_gps, match_found, True, True))
                        matched_wyscout_teams.add(match_found)
                    else:
                        team_records.append((team_gps, None, True, False))
            else:
                team_records.append((team_gps, None, True, False))
        
        # Add unmatched Wyscout teams
        for team_wyscout in teams_wyscout:
            if team_wyscout not in matched_wyscout_teams:
                team_records.append((None, team_wyscout, False, True))
        
        if team_records:
            dim_team_df = pd.DataFrame(team_records, columns=["team_name_gps", "team_name_wyscout", "has_gps", "has_wyscout"])
            dim_team_df["team_name_std"] = dim_team_df["team_name_gps"].combine_first(dim_team_df["team_name_wyscout"])
            dim_team_df.to_sql("dim_team", engine, if_exists="append", index=False)
            print(f"✓ Populated dim_team with {len(dim_team_df)} teams")
            return True
        else:
            print("⚠ No teams found to populate")
            return False
    except Exception as e:
        print(f"✗ Error populating dim_team: {e}")
        import traceback
        traceback.print_exc()
        return False

def populate_dim_competition():
    """Populate the competition dimension table from CSV files."""
    print("\n" + "=" * 80)
    print("POPULATING DIM_COMPETITION")
    print("=" * 80)
    
    try:
        # Check if already populated
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_competition"))
            count = result.scalar()
            if count > 0:
                print(f"✓ dim_competition already populated with {count} records")
                return True
        
        competitions = []
        if os.path.exists(WYSCOUT_CSV_PATH):
            try:
                wyscout_df = pd.read_csv(WYSCOUT_CSV_PATH, low_memory=False, nrows=1000)  # Sample first
                if "competition" in wyscout_df.columns:
                    competitions = wyscout_df["competition"].dropna().unique().tolist()
                print(f"  Found {len(competitions)} competitions")
            except Exception as e:
                print(f"  ⚠ Error reading Wyscout CSV: {e}")
        else:
            print(f"  ⚠ Wyscout CSV file not found: {WYSCOUT_CSV_PATH}")
        
        if competitions:
            competition_records = [{"competition_name": comp} for comp in competitions]
            dim_competition_df = pd.DataFrame(competition_records)
            dim_competition_df.to_sql("dim_competition", engine, if_exists="append", index=False)
            print(f"✓ Populated dim_competition with {len(dim_competition_df)} competitions")
            return True
        else:
            print("⚠ No competitions found to populate")
            return False
    except Exception as e:
        print(f"✗ Error populating dim_competition: {e}")
        return False

def populate_dim_player():
    """Populate the player dimension table from CSV files."""
    print("\n" + "=" * 80)
    print("POPULATING DIM_PLAYER")
    print("=" * 80)
    
    try:
        # Check if already populated
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_player"))
            count = result.scalar()
            if count > 0:
                print(f"✓ dim_player already populated with {count} records")
                return True
        
        players_gps = []
        if os.path.exists(GPS_CSV_PATH):
            try:
                gps_df = pd.read_csv(GPS_CSV_PATH, low_memory=False, nrows=1000)  # Sample first
                if "name" in gps_df.columns:
                    players_gps = gps_df["name"].dropna().unique().tolist()
                print(f"  Found {len(players_gps)} GPS players")
            except Exception as e:
                print(f"  ⚠ Error reading GPS CSV: {e}")
        else:
            print(f"  ⚠ GPS CSV file not found: {GPS_CSV_PATH}")
        
        if players_gps:
            player_records = [{"player_name_std": p, "player_name_gps": p, "player_name_wyscout": None, "has_gps": True, "has_wyscout": False} for p in players_gps]
            dim_player_df = pd.DataFrame(player_records)
            dim_player_df.to_sql("dim_player", engine, if_exists="append", index=False)
            print(f"✓ Populated dim_player with {len(dim_player_df)} players")
            return True
        else:
            print("⚠ No players found to populate")
            return False
    except Exception as e:
        print(f"✗ Error populating dim_player: {e}")
        return False

def create_fact_tables():
    """Create all fact tables."""
    print("\n" + "=" * 80)
    print("CREATING FACT TABLES")
    print("=" * 80)
    
    fact_schema_sql = """
    CREATE TABLE IF NOT EXISTS fact_player_gps (
        id INTEGER PRIMARY KEY,
        player_id INTEGER,
        team_id INTEGER,
        match_id INTEGER,
        date_id INTEGER,
        session_type VARCHAR(50),
        distance_total REAL,
        top_speed REAL,
        accelerations INTEGER,
        decelerations INTEGER,
        FOREIGN KEY (player_id) REFERENCES dim_player(player_id),
        FOREIGN KEY (team_id) REFERENCES dim_team(team_id),
        FOREIGN KEY (match_id) REFERENCES dim_match(match_id),
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
    );

    CREATE TABLE IF NOT EXISTS fact_player_wyscout (
        id INTEGER PRIMARY KEY,
        player_id INTEGER,
        team_id INTEGER,
        match_id INTEGER,
        date_id INTEGER,
        competition_id INTEGER,
        goals INTEGER,
        assists INTEGER,
        xg REAL,
        passes_total INTEGER,
        passes_completed INTEGER,
        FOREIGN KEY (player_id) REFERENCES dim_player(player_id),
        FOREIGN KEY (team_id) REFERENCES dim_team(team_id),
        FOREIGN KEY (match_id) REFERENCES dim_match(match_id),
        FOREIGN KEY (competition_id) REFERENCES dim_competition(competition_id)
    );

    CREATE TABLE IF NOT EXISTS fact_wyscout_match (
        id INTEGER PRIMARY KEY,
        team_id INTEGER,
        opponent_team_id INTEGER,
        match_id INTEGER,
        date_id INTEGER,
        competition_id INTEGER,
        possession_pct REAL,
        shots_total INTEGER,
        shots_on_target INTEGER,
        xg REAL,
        passes_total INTEGER,
        passes_completed INTEGER,
        duels_won INTEGER,
        FOREIGN KEY (team_id) REFERENCES dim_team(team_id),
        FOREIGN KEY (opponent_team_id) REFERENCES dim_team(team_id),
        FOREIGN KEY (match_id) REFERENCES dim_match(match_id),
        FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
        FOREIGN KEY (competition_id) REFERENCES dim_competition(competition_id)
    );
    """
    
    try:
        with engine.begin() as conn:
            for statement in fact_schema_sql.split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))
        print("✓ Fact tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating fact tables: {e}")
        return False

def display_database_summary():
    """Display summary of database tables and records."""
    print("\n" + "=" * 80)
    print("DATABASE SUMMARY")
    print("=" * 80)
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n✓ Database contains {len(tables)} tables:")
        
        for table_name in tables:
            try:
                columns = inspector.get_columns(table_name)
                with engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = result.scalar()
                print(f"  - {table_name}: {len(columns)} columns, {count:,} records")
            except Exception as e:
                print(f"  - {table_name}: Error reading count - {e}")
    except Exception as e:
        print(f"✗ Error displaying summary: {e}")

def main():
    """Main execution function."""
    print("=" * 80)
    print("GPS & WYSCOUT SPORTS ANALYTICS ETL PIPELINE")
    print("Database Creation and Population")
    print("=" * 80)
    
    # Test connection
    if not test_connection():
        print("\n✗ Cannot proceed without database connection")
        return
    
    # Step 1: Create dimension tables
    if not create_dimension_tables():
        print("\n✗ Failed to create dimension tables")
        return
    
    # Step 2: Populate dimension tables
    populate_dim_date()
    populate_dim_team()
    populate_dim_competition()
    populate_dim_player()
    
    # Step 3: Create fact tables
    if not create_fact_tables():
        print("\n✗ Failed to create fact tables")
        return
    
    # Step 4: Display summary
    display_database_summary()
    
    print("\n" + "=" * 80)
    print("✓ PROCESS COMPLETED!")
    print("=" * 80)
    print(f"\nDatabase file: {DB_PATH}")
    print("\nNote: Fact tables are created but not populated.")
    print("      Use populate_fact_tables.py to populate fact tables with data.")

if __name__ == "__main__":
    main()
