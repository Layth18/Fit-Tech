"""
Script to create data tables and populate them from CSV files.
Uses only standard library and SQLite (no external dependencies).
"""

import sqlite3
import csv
import os
from datetime import datetime, date, timedelta
from collections import defaultdict

# File paths
DB_PATH = "football_dw.db"
GPS_MATCHES_CSV = "hackathon/Data After Extraction/CSV/matchs_gps.csv"
GPS_TRAINING_CSV = "hackathon/Data After Extraction/CSV/training_gps.csv"
WYSCOUT_MATCHES_CSV = "hackathon/Data After Extraction/CSV/wyscout_matchs.csv"
WYSCOUT_PLAYERS_OUTFIELD_CSV = "hackathon/Data After Extraction/CSV/wyscout_players_outfield.csv"
WYSCOUT_PLAYERS_GOALKEEPER_CSV = "hackathon/Data After Extraction/CSV/wyscout_players_goalkeeper.csv"

def create_database_schema(conn):
    """Create comprehensive database schema."""
    print("=" * 80)
    print("CREATING DATABASE SCHEMA")
    print("=" * 80)
    
    cursor = conn.cursor()
    
    # Drop existing tables if needed (optional - comment out if you want to keep existing data)
    # cursor.execute("DROP TABLE IF EXISTS fact_player_gps")
    # cursor.execute("DROP TABLE IF EXISTS fact_player_wyscout")
    # cursor.execute("DROP TABLE IF EXISTS fact_wyscout_match")
    # cursor.execute("DROP TABLE IF EXISTS dim_match")
    # cursor.execute("DROP TABLE IF EXISTS dim_player")
    # cursor.execute("DROP TABLE IF EXISTS dim_team")
    # cursor.execute("DROP TABLE IF EXISTS dim_competition")
    # cursor.execute("DROP TABLE IF EXISTS dim_date")
    
    # DIM_DATE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_date DATE UNIQUE NOT NULL,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            week INTEGER,
            quarter INTEGER,
            season VARCHAR(20),
            day_of_week VARCHAR(20),
            is_weekend BOOLEAN
        )
    """)
    print("✓ Created table: dim_date")
    
    # DIM_COMPETITION
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_competition (
            competition_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_name VARCHAR(200) UNIQUE NOT NULL,
            country VARCHAR(100),
            competition_type VARCHAR(50)
        )
    """)
    print("✓ Created table: dim_competition")
    
    # DIM_TEAM
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_team (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name_std VARCHAR(200),
            team_name_gps VARCHAR(200),
            team_name_wyscout VARCHAR(200),
            has_gps BOOLEAN DEFAULT 0,
            has_wyscout BOOLEAN DEFAULT 0
        )
    """)
    print("✓ Created table: dim_team")
    
    # DIM_PLAYER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_player (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name_std VARCHAR(200),
            player_name_gps VARCHAR(200),
            player_name_wyscout VARCHAR(200),
            has_gps BOOLEAN DEFAULT 0,
            has_wyscout BOOLEAN DEFAULT 0
        )
    """)
    print("✓ Created table: dim_player")
    
    # DIM_MATCH
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_match (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        )
    """)
    print("✓ Created table: dim_match")
    
    # FACT_PLAYER_GPS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_player_gps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        )
    """)
    print("✓ Created table: fact_player_gps")
    
    # FACT_PLAYER_WYSCOUT
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_player_wyscout (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        )
    """)
    print("✓ Created table: fact_player_wyscout")
    
    # FACT_WYSCOUT_MATCH
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_wyscout_match (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        )
    """)
    print("✓ Created table: fact_wyscout_match")
    
    conn.commit()
    print("\n✓ Database schema created successfully!")

def populate_dim_date(conn):
    """Populate the date dimension table."""
    print("\n" + "=" * 80)
    print("POPULATING DIM_DATE")
    print("=" * 80)
    
    cursor = conn.cursor()
    
    # Check if already populated
    cursor.execute("SELECT COUNT(*) FROM dim_date")
    if cursor.fetchone()[0] > 0:
        print("✓ dim_date already populated")
        return
    
    start_date = date(2020, 1, 1)
    end_date = date(2026, 12, 31)
    current_date = start_date
    
    records = []
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day
        week = current_date.isocalendar()[1]
        quarter = (month - 1) // 3 + 1
        season = f"{year}-{year+1}" if month >= 7 else f"{year-1}-{year}"
        day_of_week = current_date.strftime("%A")
        is_weekend = current_date.weekday() >= 5
        
        records.append((current_date, year, month, day, week, quarter, season, day_of_week, is_weekend))
        current_date = current_date + timedelta(days=1)
    
    cursor.executemany("""
        INSERT OR IGNORE INTO dim_date 
        (full_date, year, month, day, week, quarter, season, day_of_week, is_weekend)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    
    conn.commit()
    print(f"✓ Populated dim_date with {len(records)} records")

def read_csv_file(file_path, max_rows=None):
    """Read a CSV file and return list of dictionaries."""
    if not os.path.exists(file_path):
        print(f"⚠ File not found: {file_path}")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = []
            for i, row in enumerate(reader):
                if max_rows and i >= max_rows:
                    break
                rows.append(row)
            return rows
    except Exception as e:
        print(f"⚠ Error reading {file_path}: {e}")
        return []

def populate_dim_tables(conn):
    """Populate dimension tables from CSV files."""
    print("\n" + "=" * 80)
    print("POPULATING DIMENSION TABLES FROM CSV FILES")
    print("=" * 80)
    
    cursor = conn.cursor()
    
    # Read GPS data
    print(f"\nReading GPS data from {GPS_MATCHES_CSV}...")
    gps_data = read_csv_file(GPS_MATCHES_CSV, max_rows=1000)  # Sample first
    print(f"✓ Loaded {len(gps_data)} GPS records (sample)")
    
    # Read Wyscout data
    print(f"Reading Wyscout data from {WYSCOUT_MATCHES_CSV}...")
    wyscout_data = read_csv_file(WYSCOUT_MATCHES_CSV, max_rows=1000)  # Sample first
    print(f"✓ Loaded {len(wyscout_data)} Wyscout records (sample)")
    
    # Populate dim_team
    print("\n--- Populating dim_team ---")
    teams_gps = set()
    teams_wyscout = set()
    
    for row in gps_data:
        if "team_name" in row and row["team_name"]:
            teams_gps.add(row["team_name"])
    
    for row in wyscout_data:
        if "equipe" in row and row["equipe"]:
            teams_wyscout.add(row["equipe"])
    
    # Get existing teams
    cursor.execute("SELECT team_name_std FROM dim_team")
    existing_teams = {row[0] for row in cursor.fetchall()}
    
    team_records = []
    for team_gps in teams_gps:
        if team_gps not in existing_teams:
            # Simple matching - find similar team name
            best_match = None
            best_score = 0
            for team_wyscout in teams_wyscout:
                # Simple similarity check
                common_words = set(team_gps.lower().split()) & set(team_wyscout.lower().split())
                if common_words:
                    score = len(common_words)
                    if score > best_score:
                        best_score = score
                        best_match = team_wyscout
            
            team_records.append((
                team_gps,  # team_name_std
                team_gps,  # team_name_gps
                best_match if best_score > 0 else None,  # team_name_wyscout
                1,  # has_gps
                1 if best_match else 0  # has_wyscout
            ))
            existing_teams.add(team_gps)
    
    # Add Wyscout teams not in GPS
    for team_wyscout in teams_wyscout:
        if team_wyscout not in existing_teams:
            team_records.append((
                team_wyscout,  # team_name_std
                None,  # team_name_gps
                team_wyscout,  # team_name_wyscout
                0,  # has_gps
                1  # has_wyscout
            ))
            existing_teams.add(team_wyscout)
    
    if team_records:
        cursor.executemany("""
            INSERT OR IGNORE INTO dim_team 
            (team_name_std, team_name_gps, team_name_wyscout, has_gps, has_wyscout)
            VALUES (?, ?, ?, ?, ?)
        """, team_records)
        conn.commit()
        print(f"✓ Populated dim_team with {len(team_records)} teams")
    else:
        print("✓ No new teams to add")
    
    # Populate dim_competition
    print("\n--- Populating dim_competition ---")
    competitions = set()
    for row in wyscout_data:
        if "competition" in row and row["competition"]:
            competitions.add(row["competition"])
    
    cursor.execute("SELECT competition_name FROM dim_competition")
    existing_competitions = {row[0] for row in cursor.fetchall()}
    
    competition_records = []
    for comp in competitions:
        if comp not in existing_competitions:
            competition_records.append((comp,))
    
    if competition_records:
        cursor.executemany("""
            INSERT OR IGNORE INTO dim_competition (competition_name)
            VALUES (?)
        """, competition_records)
        conn.commit()
        print(f"✓ Populated dim_competition with {len(competition_records)} competitions")
    else:
        print("✓ No new competitions to add")
    
    # Populate dim_player
    print("\n--- Populating dim_player ---")
    players_gps = set()
    for row in gps_data:
        if "name" in row and row["name"]:
            players_gps.add(row["name"])
    
    cursor.execute("SELECT player_name_std FROM dim_player")
    existing_players = {row[0] for row in cursor.fetchall()}
    
    player_records = []
    for player_gps in players_gps:
        if player_gps not in existing_players:
            player_records.append((
                player_gps,  # player_name_std
                player_gps,  # player_name_gps
                None,  # player_name_wyscout
                1,  # has_gps
                0  # has_wyscout
            ))
    
    if player_records:
        cursor.executemany("""
            INSERT OR IGNORE INTO dim_player 
            (player_name_std, player_name_gps, player_name_wyscout, has_gps, has_wyscout)
            VALUES (?, ?, ?, ?, ?)
        """, player_records)
        conn.commit()
        print(f"✓ Populated dim_player with {len(player_records)} players")
    else:
        print("✓ No new players to add")

def display_database_summary(conn):
    """Display summary of created database."""
    print("\n" + "=" * 80)
    print("DATABASE SUMMARY")
    print("=" * 80)
    
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n✓ Created {len(tables)} tables:")
    for table_name in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"  - {table_name}: {len(columns)} columns, {count} records")

def main():
    """Main execution function."""
    print("=" * 80)
    print("GPS & WYSCOUT SPORTS ANALYTICS ETL PIPELINE")
    print("Table Creation and Data Population")
    print("=" * 80)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Step 1: Create database schema
        print("\n[Step 1] Creating database schema...")
        create_database_schema(conn)
        
        # Step 2: Populate dimension tables
        print("\n[Step 2] Populating dimension tables...")
        populate_dim_date(conn)
        populate_dim_tables(conn)
        
        # Step 3: Display summary
        display_database_summary(conn)
        
        print("\n" + "=" * 80)
        print("✓ PROCESS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\nDatabase file: {DB_PATH}")
        print("\nNote: Fact tables can be populated by reading the full CSV files")
        print("      and mapping them to the dimension tables using the lookup IDs.")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()

