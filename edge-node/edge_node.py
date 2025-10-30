import sys
import requests , json
import random , time 

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

node_id = config_data.get("id", "default_node")

central_server_url = "http://localhost:8000"

# Additional edge node logic would go here# For example, initializing network connections, starting services, etc.

#register the node to the central server
print("Registering to Central Server...")
requests.post(f"{central_server_url}/node/register", json = config_data)

while True:

    try:
        if random.random() < 0.2:  # Simulate a 20% chance of failure
            raise requests.ConnectionError("Simulated connection error")

        node_updates = requests.get(f"{central_server_url}/updates/{node_id}").json()

        if(node_updates.get("version")!= config_data.get("version")):
            print("New update found. Updating...")
            config_data = node_updates
            # with open(config_file, 'w') as file:
            #     file.write(str(config_data))
            print("Update applied successfully.")

        requests.post(f"{central_server_url}/sync", data={"node_id": node_id , "version": config_data.get("version")})

    except requests.ConnectionError:
        print("Connection error occurred. Retrying...")
        
    time.sleep(random.randint(5, 10))
