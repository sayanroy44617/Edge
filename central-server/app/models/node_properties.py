from pydantic import BaseModel

class Node(BaseModel):
    id: int
    version: str
    status: str
    metrics: dict

class NodeProperties(BaseModel):
    id: str
    version: str
    last_sync: str
    status: str