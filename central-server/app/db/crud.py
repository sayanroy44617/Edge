from datetime import datetime
from sqlalchemy.orm import Session
import schemas.node
from . import models

def get_node(db: Session, node_id: str):
    """Fetch a single node by ID"""
    return db.query(models.Node).filter(models.Node.node_id == node_id).first()

def get_nodes(db: Session, skip: int = 0, limit: int = 100):
    """Fetch a list of nodes (for the dashboard)"""
    return db.query(models.Node).offset(skip).limit(limit).all()


def update_node_heartbeat(db: Session, heartbeat: schemas.node.NodeHeartbeat):
    """
    The Core Logic:
    1. Finds or Creates the Node.
    2. Updates 'last_heartbeat' to now.
    3. Saves telemetry metrics to history.
    """
    # 1. Check if Node exists
    db_node = get_node(db, node_id=heartbeat.node_id)

    if not db_node:
        # Create new Node
        db_node = models.Node(
            node_id=heartbeat.node_id,
            name=heartbeat.name,
            ip_address=heartbeat.ip_address,
            config=heartbeat.config,
            is_online=True,
            last_heartbeat=datetime.now()
        )
        db.add(db_node)
    else:
        # Update existing Node
        db_node.is_online = True
        db_node.last_heartbeat = datetime.now()
        # Update dynamic fields if provided
        if heartbeat.ip_address:
            db_node.ip_address = heartbeat.ip_address
        if heartbeat.name:
            db_node.name = heartbeat.name

    # 2. Log Telemetry (if provided in the heartbeat)
    if heartbeat.telemetry:
        db_telemetry = models.TelemetryHistory(
            node_id=heartbeat.node_id,
            cpu_percent=heartbeat.telemetry.cpu_percent,
            memory_percent=heartbeat.telemetry.memory_percent,
            disk_usage_percent=heartbeat.telemetry.disk_usage_percent,
            timestamp=datetime.utcnow()
        )
        db.add(db_telemetry)

    # 3. Commit Transaction
    db.commit()
    db.refresh(db_node)
    return db_node