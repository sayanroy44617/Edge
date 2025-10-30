from random import random
from fastapi import APIRouter
from ..models.node_properties import Node
from ..db import db_handler
import time


router = APIRouter(prefix = "/node" , tags = ["nodes"])


@router.post("/register")
def register_node(request: Node):
    db_handler.upsert_node(request.id, request.version, "active")
    return {"message": "Node registered successfully", "node": request.dict()}


@router.get("/updates/{node_id}")
def update_node(node_id: str):
    
    return {"node_id": node_id , "version": "1.1.5"}


@router.post("/sync")
def sync_node(request: Node):
    status = "healthy" if random.random() > 0.3 else "error"
    db_handler.upsert_node(request.id, request.version, status)
    return {"message": "Node synced successfully"}

@router.get("/status")
def status():
    rows = db_handler.get_all_nodes()
    return [{"id": r[0], "version": r[1],
             "last_sync": time.strftime('%H:%M:%S', time.localtime(r[2])),
             "status": r[3]} for r in rows]