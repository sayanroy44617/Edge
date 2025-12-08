from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel,ConfigDict

from schemas.TelemetryHistoryModel import TelemetryCreate


class NodeBase(BaseModel):
    node_id: str
    name: Optional[str] = None
    ip_address: Optional[str] = None
    config: Optional[Dict[str, Any]] = {}

# Create/Heartbeat: What the Agent sends
class NodeHeartbeat(NodeBase):
    telemetry: Optional[TelemetryCreate] = None

# Read: What the API returns to the dashboard
class NodeRead(NodeBase):
    is_online: bool
    last_heartbeat: datetime
    # We remove 'telemetry_logs' here to prevent loading 1000s of rows by accident.
    # We will fetch logs via a separate endpoint /nodes/{id}/telemetry


    '''this will tell pydantic to read data even if it is not a dict, but an ORM model
    node_orm = session.query(Node).first()  # SQLAlchemy ORM object
    node_schema = NodeSchema.from_orm(node_orm)  # Pydantic model instance'''
    model_config = ConfigDict(from_attributes=True)






