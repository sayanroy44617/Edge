import random
import time
import requests

metrics = {
    "cpu" : random.uniform(0, 100),
    "memory": random.uniform(0, 100),
    "disk": random.uniform(0, 100)
}

def get_health_status():
    if metrics["cpu"] < 70 and metrics["memory"] < 70 and metrics["disk"] < 70:
        return "healthy"
    else:
        return "error"
    
def get_metrics():
    return metrics

def heartbeat(id : str , central_server_url : str):
    print("sending heartbeat to central server...")
    while True:
        try:
            requests.post(f"{central_server_url}/node/heartbeat/{id}")
        except Exception:
            pass
        sleep_time = 5
        time.sleep(sleep_time)