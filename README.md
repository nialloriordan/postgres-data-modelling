# Data Modelling with Postgres

- [Data Modelling with Postgres](#data-modelling-with-postgres)
  - [Summary](#summary)
  - [Quick Start](#quick-start)
    - [Running python Scripts](#running-python-scripts)
  - [Structure](#structure)
  - [Database Schema](#database-schema)
  - [Sample Queries](#sample-queries)

## Summary

The purpose of this repo is to create a postgres database to enable data modelling for Sparkify and their collection of songs and user activity from their music streaming app. This database will enable the analytics team to analyse the data and understand what songs users are listening to.

## Quick Start
<details open>
    <summary> Show/Hide Details</summary>

### Running python Scripts

To create the postgres schema run the following processes in order from your terminal in the root directory

1. Create the postgres tables from the `create_tables` python script:   
  `python create_tables.py`

2. To run the data modelling pipeline run the `etl` python script:  
  `python etl.py`

</details>

## Structure

<details open>
    <summary> Show/Hide Details</summary>

* [data/](data/): postgres data
  * [log_data](data/log_data/): log files from user activity in JSON format
  * [dsong_data](data/song_data/): song metadata in JSON format
* [create_tables.py](create_tables.py): python script to create postgres tables
* [etl.py](etl.py): python script to run ETL processes for each table
* [sql_queries.py](sql_queries.py): helper queries to drop, create and insert data into tables
* [test notebook](test.ipynb): notebook to sample results from postgres tables
* [static/](static/): folder with static images for README

</details>

## Database Schema

<details>
    <summary> Show/Hide Details</summary>

![Postgres Schema](static/postgres_schema.svg "Postgres Schema")

</details>

## Sample Queries

<details>
    <summary> Show/Hide Details</summary>

1. Top 5 songs by number of times the song was listened to

```sql
SELECT 
  s.title as song_title, 
  a.name as artist_name, 
  COUNT(*) as listens 
FROM 
  songplays sp 
  JOIN songs s ON sp.song_id = s.song_id 
  JOIN artists a ON a.artist_id = sp.artist_id  
GROUP BY (s.title, a.name)
ORDER BY listens DESC
LIMIT 5
```

2. Top 5 artists based on number of songs that have been listened to

```sql
SELECT 
  a.name as artist_name, 
  COUNT(*) as listens 
FROM 
  songplays sp 
  JOIN artists a ON a.artist_id = sp.artist_id  
GROUP BY (a.name)
ORDER by listens DESC
LIMIT 5
```

3. Identify top 10 most active users with a free account

```sql
SELECT 
  user_id, 
  COUNT(*) as listens
FROM songplays 
WHERE level = 'free' 
GROUP BY (user_id) 
ORDER BY count DESC
LIMIT 10
```

</details>
