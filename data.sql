-- === DIMENSIONS ===
CREATE TABLE IF NOT EXISTS dim_team (
    team_id SERIAL PRIMARY KEY,
    team_name_std VARCHAR(200),
    team_name_gps VARCHAR(200),
    team_name_wyscout VARCHAR(200),
    has_gps BOOLEAN,
    has_wyscout BOOLEAN
);

CREATE TABLE IF NOT EXISTS dim_player (
    player_id SERIAL PRIMARY KEY,
    player_name_std VARCHAR(200),
    player_name_gps VARCHAR(200),
    player_name_wyscout VARCHAR(200),
    has_gps BOOLEAN,
    has_wyscout BOOLEAN
);

CREATE TABLE IF NOT EXISTS dim_match (
    match_id SERIAL PRIMARY KEY,
    match_date DATE,
    home_team VARCHAR(200),
    away_team VARCHAR(200),
    home_score INT,
    away_score INT
);

-- === FACTS ===
CREATE TABLE IF NOT EXISTS fact_player_gps (
    id SERIAL PRIMARY KEY,
    player_id INT,
    team_id INT,
    match_id INT,
    date_key DATE,
    session_type VARCHAR(50),
    total_distance_m NUMERIC,
    top_speed_kmh NUMERIC
);

CREATE TABLE IF NOT EXISTS fact_player_wyscout (
    id SERIAL PRIMARY KEY,
    player_id INT,
    match_id INT,
    team_id INT,
    minutes_played INT,
    goals INT,
    assists INT,
    xg NUMERIC
);
