"""Model with helper queries to drop, create and insert data into tables"""

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = """
CREATE TABLE IF NOT EXISTS songplays(
    songplay_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP,
    user_id INTEGER,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INTEGER,
    location VARCHAR,
    user_agent VARCHAR
)
"""

user_table_create = """
CREATE TABLE IF NOT EXISTS users(
    user_id integer PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender CHAR(1),
    level VARCHAR
)
"""

song_table_create = """
CREATE TABLE IF NOT EXISTS songs(
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    artist_id VARCHAR,
    year INTEGER,
    duration NUMERIC
)
"""

artist_table_create = """
CREATE TABLE IF NOT EXISTS artists(
    artist_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude NUMERIC,
    longitude NUMERIC
)
"""

time_table_create = """
CREATE TABLE IF NOT EXISTS time(
    start_time TIMESTAMP PRIMARY KEY,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER
)
"""

# INSERT RECORDS

songplay_table_insert = """
INSERT INTO songplays(
    start_time,
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent
) Values(%s, %s, %s, %s, %s, %s, %s, %s)
"""

user_table_insert = """
INSERT INTO users(
    user_id,
    first_name,
    last_name,
    gender,
    level
) Values(%s, %s, %s, %s, %s)
ON CONFLICT(user_id) DO UPDATE
    SET level = EXCLUDED.level
"""

song_table_insert = """
INSERT INTO songs(
    song_id,
    title,
    artist_id,
    year,
    duration
) Values(%s, %s, %s, %s, %s)
ON CONFLICT(song_id) DO NOTHING
"""

artist_table_insert = """
INSERT INTO artists(
    artist_id,
    name,
    location,
    latitude,
    longitude
) Values(%s, %s, %s, %s, %s)
ON CONFLICT(artist_id) DO NOTHING
"""


time_table_insert = """
INSERT INTO time(
    start_time,
    hour,
    day,
    week,
    month,
    year,
    weekday
) Values(%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING
"""

# FIND SONGS

song_select = """
SELECT 
    songs.song_id, 
    songs.artist_id
FROM songs
JOIN artists
    ON artists.artist_id = songs.artist_id
WHERE (
        songs.title = %s AND
        artists.name = %s AND
        songs.duration = %s
)
"""

# QUERY LISTS

create_table_queries = [
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]
drop_table_queries = [
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]
