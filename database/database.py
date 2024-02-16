import sqlite3
from sqlite3 import Connection

DATABASE_URL = "data/sqlite.db"

def get_db_connection() -> Connection:
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firing_profiles (
        id INTEGER PRIMARY KEY,
        profile_name TEXT NOT NULL,
        temperature_target REAL NOT NULL,
        hold_time INTEGER NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperature_data (
        id INTEGER PRIMARY KEY,
        temperature REAL NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_firing_profile(profile_data: dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO firing_profiles (profile_name, temperature_target, hold_time)
    VALUES (:profile_name, :temperature_target, :hold_time)
    """, profile_data)
    conn.commit()
    conn.close()

def list_firing_profiles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM firing_profiles")
    profiles = cursor.fetchall()
    conn.close()
    return [dict(profile) for profile in profiles]

def get_firing_profile(profile_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM firing_profiles WHERE profile_name = ?", (profile_name,))
    profile = cursor.fetchone()
    conn.close()
    return dict(profile) if profile else None

# Call init_db() to initialize the database at the start of your application
init_db()
