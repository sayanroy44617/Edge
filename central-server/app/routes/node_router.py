from fastapi import APIRouter
from ..models.node_properties import Node
from ..db import db_handler
import time , requests , random


router = APIRouter(prefix = "/node" , tags = ["nodes"])


@router.post("/register")
def register_node(request: Node):
    db_handler.register_node(request)
    return {"message": "Node registered successfully", "node": request.dict()}


@router.get("/updates/{node_id}")
def update_node(node_id: str):
    return {"node_id": node_id , "version": "1.1.5"}


@router.post("/sync")
def sync_node(request: Node):
    db_handler.update_node(request)
    return {"message": "Node synced successfully"}

@router.get("/status")
def status():
    rows = db_handler.get_all_nodes()
    return [{"id": r[0], "version": r[1],
             "status": r[2],
             "metrics": eval(r[3]),
             "last_sync": time.strftime('%H:%M:%S', time.localtime(r[5])) if r[5] else None,
             "registered_at": time.strftime('%H:%M:%S', time.localtime(r[4])) if r[4] else None,
             "last_seen": time.strftime('%H:%M:%S', time.localtime(r[6])) if r[6] else None
             } for r in rows]

@router.post("/heartbeat/{node_id}")
def send_heartbeat(node_id: str):
    db_handler.update_heartbeat(node_id)
    return {"message": "Heartbeat received"}