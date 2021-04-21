"""Model to create postgres tables"""

import psycopg2
from sql_queries import create_table_queries, drop_table_queries
from dotenv import load_dotenv
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(dotenv_path=os.path.join(dir_path, ".env"))
# Db connection details
PG_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
PG_USER = os.getenv("POSTGRES_USER", "student")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "student")


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """

    # connect to default database
    conn = psycopg2.connect(
        f"host={PG_HOST} dbname=studentdb user={PG_USER} password={PG_PASSWORD}"
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect(
        f"host={PG_HOST} dbname=sparkifydb user={PG_USER} password={PG_PASSWORD}"
    )
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.

    - Establishes connection with the sparkify database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()