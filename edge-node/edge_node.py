import sys
import requests , json , threading
import random , time 
from metrics import get_health_status , get_metrics, heartbeat

config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"

try:
    with open(config_file, 'r') as file:
        config_data = json.loads(file.read())
        print("Configuration Data:")
        print(json.dumps(config_data, indent=4))
except FileNotFoundError:
    print(f"Configuration file '{config_file}' not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error decoding JSON from the configuration file '{config_file}'.")
    sys.exit(1)

id = config_data.get("id", "default_node")

central_server_url = "http://localhost:8000"

threading.Thread(target=heartbeat, args=(id, central_server_url), daemon=True).start()

# Additional edge node logic would go here# For example, initializing network connections, starting services, etc.

#register the node to the central server
config_data["status"] = get_health_status()
config_data["metrics"] = get_metrics()

print("Registering to Central Server...")
requests.post(f"{central_server_url}/node/register", json = config_data)

while True:

    print("Checking for updates...")

    try:
        if random.random() < 0.1:  # Simulate a 10% chance of failure
            raise requests.ConnectionError("Simulated connection error")

        node_updates = requests.get(f"{central_server_url}/node/updates/{id}").json()

        if(node_updates.get("version")!= config_data.get("version")):
            print("New update found. Updating...")
            config_data = node_updates
            print(type(config_data))
            with open(config_file, 'w') as file:
                json.dump(config_data, file, indent=4)
            print("Update applied successfully.")

        config_data["status"] = get_health_status()
        config_data["metrics"] = get_metrics()
        requests.post(f"{central_server_url}/node/sync", json=config_data)

    except requests.ConnectionError:
        print("Connection error occurred. Retrying...")
        
    time.sleep(random.randint(30 , 60))
