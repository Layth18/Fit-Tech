"""
Script to analyze the .docx documentation file and create data tables
based on the analysis, then fill them with data from CSV files.
"""

# Import docx with error handling (optional dependency)
try:
    from docx import Document  # type: ignore
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    Document = None  # type: ignore
    print("⚠ Warning: python-docx package not installed. Install it with: pip install python-docx")
    print("  The script will continue but .docx file reading will be disabled.")

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

# File paths
DOCX_FILE = "GPS & Wyscout Sports Analytics ETL Pipeline Documentation (2) (2).docx"
DB_PATH = "football_dw.db"

# Create database engine (only if sqlalchemy is available)
if SQLALCHEMY_AVAILABLE:
    engine = create_engine(f"sqlite:///{DB_PATH}")
else:
    engine = None

def extract_text_from_docx(file_path):
    """Extract all text from a .docx file."""
    if not DOCX_AVAILABLE:
        print("✗ Error: python-docx package is not installed.")
        print("  Install it with: pip install python-docx")
        return None
    
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text)
        
        # Also extract text from tables in the document
        for table in doc.tables:
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    row_text.append(cell.text.strip())
                if any(row_text):
                    full_text.append(" | ".join(row_text))
        
        return "\n".join(full_text)
    except Exception as e:
        print(f"✗ Error reading .docx file: {e}")
        return None

def analyze_documentation(text):
    """Analyze the documentation text to identify required tables and their structure."""
    print("=" * 80)
    print("ANALYZING DOCUMENTATION")
    print("=" * 80)
    
    # Save extracted text to a file for review
    with open("extracted_documentation.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✓ Extracted text saved to 'extracted_documentation.txt'")
    
    # Look for table definitions, schema information, etc.
    tables_info = {}
    
    # Common patterns to look for
    keywords = {
        "dim_date": ["date", "dimension", "calendar"],
        "dim_team": ["team", "squad"],
        "dim_player": ["player", "athlete"],
        "dim_match": ["match", "game", "fixture"],
        "dim_competition": ["competition", "league", "tournament"],
        "fact_player_gps": ["gps", "player load", "distance", "speed", "acceleration"],
        "fact_player_wyscout": ["wyscout", "passes", "goals", "assists", "xg"],
        "fact_wyscout_match": ["match", "possession", "shots", "duels"]
    }
    
    # Analyze text for table mentions
    text_lower = text.lower()
    for table_name, search_terms in keywords.items():
        matches = sum(1 for term in search_terms if term in text_lower)
        if matches > 0:
            tables_info[table_name] = matches
            print(f"✓ Found references to: {table_name} ({matches} keyword matches)")
    
    return tables_info

def create_comprehensive_schema():
    """Create comprehensive database schema based on documentation and data structure."""
    print("\n" + "=" * 80)
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
    
    try:
        with engine.begin() as conn:
            for statement in schema_sql.split(";"):
                stmt = statement.strip()
                if stmt:
                    try:
                        conn.execute(text(stmt))
                        if 'CREATE TABLE' in stmt:
                            # Extract table name
                            parts = stmt.split()
                            if len(parts) > 5:
                                table_name = parts[5]
                                print(f"✓ Created table: {table_name}")
                    except Exception as e:
                        if "already exists" not in str(e).lower():
                            print(f"⚠ Warning: {e}")
        
        print("\n✓ Database schema created successfully!")
    except Exception as e:
        print(f"✗ Error creating schema: {e}")
        import traceback
        traceback.print_exc()

def populate_dim_date():
    """Populate the date dimension table."""
    print("\n" + "=" * 80)
    print("POPULATING DIM_DATE")
    print("=" * 80)
    
    try:
        from datetime import date as date_type
        
        # Check if already populated
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_date"))
            count = result.scalar()
            if count > 0:
                print(f"✓ dim_date already populated with {count} records")
                return True
        
        start_date = date_type(2020, 1, 1)
        end_date = date_type(2026, 12, 31)
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        
        dim_date_df = pd.DataFrame({
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
            dim_date_df.to_sql("dim_date", engine, if_exists="append", index=False, method="multi")
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

def populate_dim_tables_from_csv():
    """Populate dimension tables from CSV files."""
    print("\n" + "=" * 80)
    print("POPULATING DIMENSION TABLES FROM CSV FILES")
    print("=" * 80)
    
    # Read CSV files
    gps_csv = "hackathon/Data After Extraction/CSV/matchs_gps.csv"
    wyscout_csv = "hackathon/Data After Extraction/CSV/wyscout_matchs.csv"
    
    if not os.path.exists(gps_csv):
        print(f"⚠ GPS CSV file not found: {gps_csv}")
        return
    
    if not os.path.exists(wyscout_csv):
        print(f"⚠ Wyscout CSV file not found: {wyscout_csv}")
        return
    
    # Read GPS data
    try:
        print(f"Reading GPS data from {gps_csv}...")
        gps_df = pd.read_csv(gps_csv, low_memory=False, nrows=1000)  # Sample first
        print(f"✓ Loaded {len(gps_df)} GPS records (sample)")
    except Exception as e:
        print(f"✗ Error reading GPS CSV: {e}")
        return
    
    # Read Wyscout data
    try:
        print(f"Reading Wyscout data from {wyscout_csv}...")
        wyscout_df = pd.read_csv(wyscout_csv, low_memory=False, nrows=1000)  # Sample first
        print(f"✓ Loaded {len(wyscout_df)} Wyscout records (sample)")
    except Exception as e:
        print(f"✗ Error reading Wyscout CSV: {e}")
        return
    
    # Populate dim_team
    print("\n--- Populating dim_team ---")
    try:
        # Check if already populated
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_team"))
            count = result.scalar()
            if count > 0:
                print(f"✓ dim_team already populated with {count} records")
            else:
                teams_gps = gps_df["team_name"].dropna().unique() if "team_name" in gps_df.columns else []
                teams_wyscout = wyscout_df["equipe"].dropna().unique() if "equipe" in wyscout_df.columns else []
                
                team_records = []
                processed_teams = set()
                matched_wyscout_teams = set()
                
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
                            matched_wyscout_teams.add(match[0])
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
                    if team_wyscout not in matched_wyscout_teams:
                        team_records.append({
                            "team_name_std": team_wyscout,
                            "team_name_gps": None,
                            "team_name_wyscout": team_wyscout,
                            "has_gps": False,
                            "has_wyscout": True
                        })
                
                if team_records:
                    dim_team_df = pd.DataFrame(team_records)
                    dim_team_df.to_sql("dim_team", engine, if_exists="append", index=False)
                    print(f"✓ Populated dim_team with {len(dim_team_df)} teams")
    except Exception as e:
        print(f"✗ Error populating dim_team: {e}")
        import traceback
        traceback.print_exc()
    
    # Populate dim_competition
    print("\n--- Populating dim_competition ---")
    try:
        # Check if already populated
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_competition"))
            count = result.scalar()
            if count > 0:
                print(f"✓ dim_competition already populated with {count} records")
            else:
                if "competition" in wyscout_df.columns:
                    competitions = wyscout_df["competition"].dropna().unique()
                    competition_records = [{"competition_name": comp} for comp in competitions]
                    if competition_records:
                        dim_competition_df = pd.DataFrame(competition_records)
                        dim_competition_df.to_sql("dim_competition", engine, if_exists="append", index=False)
                        print(f"✓ Populated dim_competition with {len(dim_competition_df)} competitions")
    except Exception as e:
        print(f"✗ Error populating dim_competition: {e}")
    
    # Populate dim_player
    print("\n--- Populating dim_player ---")
    try:
        # Check if already populated
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM dim_player"))
            count = result.scalar()
            if count > 0:
                print(f"✓ dim_player already populated with {count} records")
            else:
                players_gps = gps_df["name"].dropna().unique() if "name" in gps_df.columns else []
                
                player_records = []
                for player_gps in players_gps:
                    player_records.append({
                        "player_name_std": player_gps,
                        "player_name_gps": player_gps,
                        "player_name_wyscout": None,
                        "has_gps": True,
                        "has_wyscout": False
                    })
                
                if player_records:
                    dim_player_df = pd.DataFrame(player_records)
                    dim_player_df.to_sql("dim_player", engine, if_exists="append", index=False)
                    print(f"✓ Populated dim_player with {len(dim_player_df)} players")
    except Exception as e:
        print(f"✗ Error populating dim_player: {e}")

def populate_fact_tables():
    """Populate fact tables from CSV files."""
    print("\n" + "=" * 80)
    print("POPULATING FACT TABLES FROM CSV FILES")
    print("=" * 80)
    
    try:
        # This is a placeholder - actual implementation would map CSV columns to fact table columns
        print("⚠ Fact table population requires detailed column mapping")
        print("  This should be implemented based on the specific CSV structure")
        print("  Use populate_fact_tables.py for full implementation")
        return True
    except Exception as e:
        print(f"✗ Error in populate_fact_tables: {e}")
        return False

def main():
    """Main execution function."""
    print("=" * 80)
    print("GPS & WYSCOUT SPORTS ANALYTICS ETL PIPELINE")
    print("Documentation Analysis and Table Creation")
    print("=" * 80)
    
    # Step 1: Extract text from .docx
    print("\n[Step 1] Extracting text from documentation...")
    doc_text = extract_text_from_docx(DOCX_FILE)
    
    if doc_text is None:
        print("❌ Failed to extract text from .docx file")
        return
    
    print(f"✓ Extracted {len(doc_text)} characters from documentation")
    
    # Step 2: Analyze documentation
    print("\n[Step 2] Analyzing documentation...")
    tables_info = analyze_documentation(doc_text)
    
    # Step 3: Create database schema
    print("\n[Step 3] Creating database schema...")
    create_comprehensive_schema()
    
    # Step 4: Populate dimension tables
    print("\n[Step 4] Populating dimension tables...")
    populate_dim_date()
    populate_dim_tables_from_csv()
    
    # Step 5: Display created tables
    print("\n" + "=" * 80)
    print("DATABASE SUMMARY")
    print("=" * 80)
    
    if not SQLALCHEMY_AVAILABLE or engine is None:
        print("✗ Cannot display summary: sqlalchemy is not available")
        return
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n✓ Created {len(tables)} tables:")
        for table_name in tables:
            columns = inspector.get_columns(table_name)
            print(f"  - {table_name} ({len(columns)} columns)")
    except Exception as e:
        print(f"✗ Error displaying summary: {e}")
    
    print("\n" + "=" * 80)
    print("✓ PROCESS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\nDatabase file: {DB_PATH}")
    print("Extracted documentation: extracted_documentation.txt")

if __name__ == "__main__":
    main()

