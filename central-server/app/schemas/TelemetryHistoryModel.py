from datetime import datetime

from pydantic import BaseModel,Field,ConfigDict

class TelemetryBaseModel(BaseModel):
    cpu_percent: float = Field(..., ge=0.0, le=100.0)
    memory_percent: float = Field(..., ge=0.0, le=100.0)
    disk_usage_percent: float = Field(..., ge=0.0, le=100.0)

class TelemetryCreate(TelemetryBaseModel):
    pass

# Read: What the DB returns (Has ID and Timestamp)
class TelemetryRead(TelemetryBaseModel):
    id: int
    node_id: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


