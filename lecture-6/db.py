import sqlite3

DB_NAME = "weather.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area_code TEXT,
        date TEXT,
        weather TEXT,
        temp_min INTEGER,
        temp_max INTEGER,
        UNIQUE(area_code, date)
    )
    """)

    conn.commit()
    conn.close()


def save_forecast(area_code, date, weather, temp_min, temp_max):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO forecasts
        (area_code, date, weather, temp_min, temp_max)
        VALUES (?, ?, ?, ?, ?)
    """, (area_code, date, weather, temp_min, temp_max))

    conn.commit()
    conn.close()


def load_forecasts(area_code):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT date, weather, temp_min, temp_max
        FROM forecasts
        WHERE area_code = ?
        ORDER BY date
        LIMIT 5
    """, (area_code,))

    rows = cur.fetchall()
    conn.close()
    return rows
def load_forecast_by_date(area_code, date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT date, weather, temp_min, temp_max
        FROM forecasts
        WHERE area_code = ?
        AND date = ?
    """, (area_code, date))

    row = cur.fetchone()
    conn.close()
    return row
