"""
Script to populate fact tables from CSV files.
"""

import sqlite3
import csv
import os
from datetime import datetime

# File paths
DB_PATH = "football_dw.db"
GPS_MATCHES_CSV = "hackathon/Data After Extraction/CSV/matchs_gps.csv"
GPS_TRAINING_CSV = "hackathon/Data After Extraction/CSV/training_gps.csv"
WYSCOUT_MATCHES_CSV = "hackathon/Data After Extraction/CSV/wyscout_matchs.csv"

def get_lookup_dicts(conn):
    """Get lookup dictionaries from dimension tables."""
    cursor = conn.cursor()
    
    # Team lookups
    cursor.execute("SELECT team_id, team_name_gps, team_name_wyscout FROM dim_team")
    team_lookup_gps = {}
    team_lookup_wyscout = {}
    for row in cursor.fetchall():
        team_id, name_gps, name_wyscout = row
        if name_gps:
            team_lookup_gps[name_gps] = team_id
        if name_wyscout:
            team_lookup_wyscout[name_wyscout] = team_id
    
    # Player lookup
    cursor.execute("SELECT player_id, player_name_gps FROM dim_player")
    player_lookup = {name: pid for pid, name in cursor.fetchall() if name}
    
    # Competition lookup
    cursor.execute("SELECT competition_id, competition_name FROM dim_competition")
    competition_lookup = {name: cid for cid, name in cursor.fetchall()}
    
    # Date lookup
    cursor.execute("SELECT date_id, full_date FROM dim_date")
    date_lookup = {}
    for row in cursor.fetchall():
        date_id, full_date = row
        if full_date:
            date_lookup[str(full_date)] = date_id
    
    return team_lookup_gps, team_lookup_wyscout, player_lookup, competition_lookup, date_lookup

def parse_date(date_str):
    """Parse date string to date object."""
    if not date_str:
        return None
    try:
        # Try different date formats
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%d-%m-%Y']:
            try:
                return datetime.strptime(str(date_str).strip(), fmt).date()
            except:
                continue
        return None
    except:
        return None

def safe_float(value):
    """Safely convert value to float."""
    if value is None or value == '' or value == 'n/a':
        return None
    try:
        return float(value)
    except:
        return None

def safe_int(value):
    """Safely convert value to int."""
    if value is None or value == '' or value == 'n/a':
        return None
    try:
        return int(float(value))
    except:
        return None

def populate_fact_player_gps(conn):
    """Populate fact_player_gps table."""
    print("\n" + "=" * 80)
    print("POPULATING FACT_PLAYER_GPS")
    print("=" * 80)
    
    if not os.path.exists(GPS_MATCHES_CSV):
        print(f"⚠ GPS CSV file not found: {GPS_MATCHES_CSV}")
        return
    
    cursor = conn.cursor()
    team_lookup_gps, _, player_lookup, _, date_lookup = get_lookup_dicts(conn)
    
    print(f"Reading {GPS_MATCHES_CSV}...")
    records = []
    row_count = 0
    
    try:
        with open(GPS_MATCHES_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_count += 1
                if row_count % 1000 == 0:
                    print(f"  Processing row {row_count}...")
                
                # Get IDs
                player_id = player_lookup.get(row.get("name"))
                team_id = team_lookup_gps.get(row.get("team_name"))
                
                # Parse date
                date_str = row.get("date")
                date_id = None
                if date_str:
                    date_obj = parse_date(date_str)
                    if date_obj:
                        date_id = date_lookup.get(str(date_obj))
                
                # Extract GPS metrics
                record = (
                    player_id,
                    team_id,
                    None,  # match_id
                    date_id,
                    row.get("type_session"),
                    row.get("report_type"),
                    row.get("type_session"),
                    row.get("gameweek"),
                    row.get("opponent"),
                    safe_float(row.get("Total Distance (m)")),
                    safe_float(row.get("Maximum Velocity (km/h)")),
                    safe_int(row.get("Acceleration B1 Efforts (Gen 2)")),
                    safe_int(row.get("Deceleration B1 Efforts (Gen 2)")),
                    safe_float(row.get("Average Velocity (km/h)")),
                    safe_float(row.get("Max Acceleration")),
                    safe_float(row.get("Max Deceleration")),
                    safe_float(row.get("Total Player Load")),
                    safe_float(row.get("Avg Heart Rate")),
                    safe_float(row.get("Maximum Heart Rate"))
                )
                
                records.append(record)
                
                # Insert in batches
                if len(records) >= 1000:
                    cursor.executemany("""
                        INSERT INTO fact_player_gps 
                        (player_id, team_id, match_id, date_id, session_type, report_type, 
                         type_session, gameweek, opponent, total_distance_m, top_speed_kmh,
                         accelerations, decelerations, average_speed_kmh, max_acceleration,
                         max_deceleration, player_load_total, heart_rate_avg, heart_rate_max)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, records)
                    conn.commit()
                    print(f"  Inserted {len(records)} records...")
                    records = []
        
        # Insert remaining records
        if records:
            cursor.executemany("""
                INSERT INTO fact_player_gps 
                (player_id, team_id, match_id, date_id, session_type, report_type, 
                 type_session, gameweek, opponent, total_distance_m, top_speed_kmh,
                 accelerations, decelerations, average_speed_kmh, max_acceleration,
                 max_deceleration, player_load_total, heart_rate_avg, heart_rate_max)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, records)
            conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM fact_player_gps")
        count = cursor.fetchone()[0]
        print(f"✓ Populated fact_player_gps with {count} records")
        
    except Exception as e:
        print(f"⚠ Error populating fact_player_gps: {e}")
        import traceback
        traceback.print_exc()

def populate_fact_wyscout_match(conn):
    """Populate fact_wyscout_match table."""
    print("\n" + "=" * 80)
    print("POPULATING FACT_WYSCOUT_MATCH")
    print("=" * 80)
    
    if not os.path.exists(WYSCOUT_MATCHES_CSV):
        print(f"⚠ Wyscout CSV file not found: {WYSCOUT_MATCHES_CSV}")
        return
    
    cursor = conn.cursor()
    _, team_lookup_wyscout, _, competition_lookup, date_lookup = get_lookup_dicts(conn)
    
    print(f"Reading {WYSCOUT_MATCHES_CSV}...")
    records = []
    row_count = 0
    
    try:
        with open(WYSCOUT_MATCHES_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row_count += 1
                if row_count % 1000 == 0:
                    print(f"  Processing row {row_count}...")
                
                # Get IDs
                team_id = team_lookup_wyscout.get(row.get("equipe"))
                opponent_id = team_lookup_wyscout.get(row.get("adversaire"))
                competition_id = competition_lookup.get(row.get("competition"))
                
                # Parse date
                date_str = row.get("date")
                date_id = None
                if date_str:
                    date_obj = parse_date(date_str)
                    if date_obj:
                        date_id = date_lookup.get(str(date_obj))
                
                # Parse score
                score_str = row.get("score", "")
                goals_scored = None
                goals_conceded = None
                if score_str and ":" in str(score_str):
                    try:
                        parts = str(score_str).split(":")
                        if len(parts) == 2:
                            goals_scored = safe_int(parts[0].strip())
                            goals_conceded = safe_int(parts[1].strip())
                    except:
                        pass
                
                record = (
                    team_id,
                    opponent_id,
                    None,  # match_id
                    date_id,
                    competition_id,
                    row.get("formation"),
                    safe_float(row.get("general_possession_pct")),
                    safe_int(row.get("general_tirs_total")),
                    safe_int(row.get("general_tirs_cadres")),
                    safe_float(row.get("general_xg")),
                    safe_int(row.get("general_passes_total")),
                    safe_int(row.get("general_passes_precises")),
                    safe_float(row.get("general_passes_precises_pct")),
                    safe_int(row.get("general_duels_gagnes")),
                    safe_int(row.get("general_duels_total")),
                    goals_scored,
                    goals_conceded
                )
                
                records.append(record)
                
                # Insert in batches
                if len(records) >= 1000:
                    cursor.executemany("""
                        INSERT INTO fact_wyscout_match 
                        (team_id, opponent_team_id, match_id, date_id, competition_id,
                         formation, possession_pct, shots_total, shots_on_target, xg,
                         passes_total, passes_completed, passes_accuracy_pct,
                         duels_won, duels_total, goals_scored, goals_conceded)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, records)
                    conn.commit()
                    print(f"  Inserted {len(records)} records...")
                    records = []
        
        # Insert remaining records
        if records:
            cursor.executemany("""
                INSERT INTO fact_wyscout_match 
                (team_id, opponent_team_id, match_id, date_id, competition_id,
                 formation, possession_pct, shots_total, shots_on_target, xg,
                 passes_total, passes_completed, passes_accuracy_pct,
                 duels_won, duels_total, goals_scored, goals_conceded)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, records)
            conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM fact_wyscout_match")
        count = cursor.fetchone()[0]
        print(f"✓ Populated fact_wyscout_match with {count} records")
        
    except Exception as e:
        print(f"⚠ Error populating fact_wyscout_match: {e}")
        import traceback
        traceback.print_exc()

def display_summary(conn):
    """Display database summary."""
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
    
    print(f"\n✓ Database contains {len(tables)} tables:")
    for table_name in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"  - {table_name}: {len(columns)} columns, {count:,} records")

def main():
    """Main execution function."""
    print("=" * 80)
    print("POPULATING FACT TABLES")
    print("=" * 80)
    
    conn = sqlite3.connect(DB_PATH)
    
    try:
        # Populate fact tables
        populate_fact_player_gps(conn)
        populate_fact_wyscout_match(conn)
        
        # Display summary
        display_summary(conn)
        
        print("\n" + "=" * 80)
        print("✓ PROCESS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"Database file: {DB_PATH}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()

