import sqlite3, time
from ..models.node_properties import Node
from ..models.node_properties import Node
DB_PATH = "controller.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS nodes")
    cur.execute("""CREATE TABLE IF NOT EXISTS nodes (
        id TEXT PRIMARY KEY,
        version TEXT,
        status TEXT,
        metrics TEXT,
        registered_at REAL,
        last_sync_at REAL,
        last_seen_at REAL
    )""")
    conn.commit()

init_db()

def get_all_nodes():
    cur = conn.cursor()
    cur.execute("SELECT * FROM nodes")
    return cur.fetchall()

def register_node(node: Node):
    with conn : 
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO nodes VALUES (?, ?, ?, ?, ?, ?, ?)",
                (node.id, node.version, node.status, str(node.metrics), time.time(), None, None))

def update_heartbeat(node_id: str):
    with conn :
        cur = conn.cursor()
        cur.execute("UPDATE nodes SET last_seen_at = ? WHERE id = ?", (time.time(), node_id))

def update_node(node: Node):
    with conn :
        cur = conn.cursor()
        cur.execute("UPDATE nodes SET version = ?, status = ?, metrics = ?, last_sync_at = ? WHERE id = ?",
                    (node.version, node.status, str(node.metrics), time.time(), node.id))

