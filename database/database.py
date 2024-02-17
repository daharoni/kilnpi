import sqlite3
from sqlite3 import Connection

DATABASE_URL = "data/sqlite.db"

# Simulated database of firing profiles
FIRING_PROFILES = [
    {"id": 1, "name": "Low Fire", "max_temperature": 1000.0, "temperature_profile": [
        {"time": 0, "temperature": 20.0},
        {"time": 60, "temperature": 100.0},
        {"time": 120, "temperature": 300.0},
        {"time": 180, "temperature": 500.0},
        {"time": 240, "temperature": 400.0},
        {"time": 300, "temperature": 200.0},
        {"time": 360, "temperature": 10.0},]},
    {"id": 2, "name": "Mid Fire", "max_temperature": 1200.0, "temperature_profile": [
        {"time": 0, "temperature": 20.0},
        {"time": 60, "temperature": 200.0},
        {"time": 120, "temperature": 500.0},
        {"time": 180, "temperature": 1300.0},
        {"time": 240, "temperature": 800.0},
        {"time": 300, "temperature": 400.0},
        {"time": 360, "temperature": 100.0},]},
]

def get_firing_profiles():
    return FIRING_PROFILES

def get_profile_by_id(profile_id: int):
    return next((profile for profile in FIRING_PROFILES if profile['id'] == profile_id), None)


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

""" def get_firing_profile(profile_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM firing_profiles WHERE profile_name = ?", (profile_name,))
    profile = cursor.fetchone()
    conn.close()
    return dict(profile) if profile else None """
# Placeholder functions for database interactions

def get_past_firing_data(profile_id: int):
    # Simulate fetching past firing data based on profile_id
    return {"id": profile_id, "data": [200, 400, 600, 800, 1000]}


# Call init_db() to initialize the database at the start of your application
init_db()
