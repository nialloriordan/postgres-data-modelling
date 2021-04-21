"""Model to run postgres data modelling"""

import os
import glob
import psycopg2
import pandas as pd
from sql_queries import (
    songplay_table_insert,
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
    song_select,
)
from typing import Callable
from dotenv import load_dotenv
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(dotenv_path=os.path.join(dir_path, ".env"))
# Db connection details
PG_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
PG_USER = os.getenv("POSTGRES_USER", "student")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "student")


def process_song_file(cur: psycopg2.extensions.cursor, filepath: str):
    """Process individual song file and insert into database

    Args:
        cur (psycopg2.extensions.cursor): postgres cursor
        filepath (str): song filepath
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(
        df[["song_id", "title", "artist_id", "year", "duration"]].values[0]
    )
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = list(
        df[
            [
                "artist_id",
                "artist_name",
                "artist_location",
                "artist_latitude",
                "artist_longitude",
            ]
        ].values[0]
    )
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur: psycopg2.extensions.cursor, filepath: str):
    """Process log file and insert into database

    Args:
        cur (psycopg2.extensions.cursor): postgres cursor
        filepath (str): log filepath
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit="ms")

    # insert time data records
    time_data = list(
        (
            list(t.values),
            list(t.dt.hour.values),
            list(t.dt.day.values),
            list(t.dt.week.values),
            list(t.dt.month.values),
            list(t.dt.year.values),
            list(t.dt.weekday.values),
        )
    )
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")

    # create time df from dictionary
    time_df = pd.DataFrame({k: v for k, v in zip(column_labels, time_data)})

    for _, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for _, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for _, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            pd.to_datetime(row.ts),
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent,
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(
    cur: psycopg2.extensions.cursor,
    conn: psycopg2.extensions.connection,
    filepath: str,
    func: Callable,
):
    """Process all data within a given directory
    with a provided function

    Args:
        cur (psycopg2.extensions.cursor): postgres cursor
        conn (psycopg2.extensions.connection): postgres connection
        filepath (str): filepath to data directory to process
        func (Callable): function to call to either porcess log files
            or user data

    Raises:
        Exception: raises an exception if an error occurs when processing the data
    """
    # get all files matching extension from directory
    all_files = []
    for root, _, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    # iterate over files and process
    try:
        for i, datafile in enumerate(all_files, 1):
            func(cur, datafile)
            conn.commit()
            print(f"{i}/{num_files} files processed.")
    except:
        raise Exception(f"Error processing: {datafile}")


def main():
    conn = psycopg2.connect(
        f"host={PG_HOST} dbname=studentdb user={PG_USER} password={PG_PASSWORD}"
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath="data/song_data", func=process_song_file)
    process_data(cur, conn, filepath="data/log_data", func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()