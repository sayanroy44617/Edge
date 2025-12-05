from sqlalchemy import Column , String, Boolean, DateTime, JSON , Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from sqlalchemy.sql.sqltypes import Text

from .database import Base

class Node(Base):

    """Represents a docker host or container monitored in the distributed system."""
    __tablename__ = "nodes"
    # Identity
    node_id = Column(String, primary_key=True, index=True) # e.g., "prod-api-01"
    name = Column(String, nullable=True)

    # Network Status
    ip_address = Column(String, nullable=True)
    is_online = Column(Boolean, default=False)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)

    # MCP Configuration (e.g., {"allowed_tools": ["restart", "logs"], "environment": "prod"})
    # This ensures we don't run dangerous tools on the wrong servers.
    config = Column(JSON, default={})

    # Relationships
    telemetry_logs = relationship("TelemetryHistory", back_populates="node", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="node", cascade="all, delete-orphan")


    # --- 2. The Vitals (Metrics) ---
class TelemetryHistory(Base):
    """
    Time-series data. The AI analyzes this to find anomalies.
    """
    __tablename__ = "telemetry_history"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("nodes.node_id"))
    timestamp = Column(DateTime, default=datetime.now(), index=True)

    # Raw Metrics
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    disk_usage_percent = Column(Float)

    # Relationship
    node = relationship("Node", back_populates="telemetry_logs")

    # --- 3. The Brain (Incidents & Self-Healing) ---
class Incident(Base):
    """
    The Core SRE Sentinel Model.
    Stores the AI analysis and the executed MCP actions.
    """
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("nodes.node_id"))

    # Status Tracking
    status = Column(String, default="OPEN") # OPEN, ANALYZING, FIXING, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Step 1: AI Analysis
    detected_anomaly = Column(Text, nullable=True)    # e.g. "Memory Leak detected pattern"
    root_cause_analysis = Column(Text, nullable=True) # LLM explanation of WHY

    # Step 2: The Cure (MCP Action)
    # Stores the JSON for the tool call: {"tool": "restart_container", "args": {"container_id": "..."}}
    recommended_fix_action = Column(JSON, nullable=True)

    # Step 3: Result
    fix_execution_result = Column(Text, nullable=True) # "Success: Container restarted in 200ms"

    # Relationship
    node = relationship("Node", back_populates="incidents")