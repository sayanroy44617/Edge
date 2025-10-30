from pydantic import BaseModel

class Node(BaseModel):
    id: int
    version: str

class NodeProperties(BaseModel):
    id: str
    version: str
    last_sync: str
    status: str