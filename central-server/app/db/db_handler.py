import sqlite3, time

DB_PATH = "controller.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    version TEXT,
    last_sync REAL,
    status TEXT
)""")
conn.commit()

def upsert_node(id, version, status):
    cur.execute("INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?)",
                (id, version, time.time(), status))
    conn.commit()

def get_all_nodes():
    cur.execute("SELECT * FROM nodes")
    return cur.fetchall()

