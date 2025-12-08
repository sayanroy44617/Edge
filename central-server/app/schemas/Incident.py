from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum

class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    ANALYZING = "ANALYZING"
    FIXING = "FIXING"
    RESOLVED = "RESOLVED"


class IncidentBase(BaseModel):
    status: IncidentStatus = IncidentStatus.OPEN
    detected_anomaly: Optional[str] = None
    root_cause_analysis: Optional[str] = None
    recommended_fix_action: Optional[Dict[str, Any]] = None
    fix_execution_result: Optional[str] = None

