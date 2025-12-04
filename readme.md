🌊 EdgeFlow: Distributed Data Pipeline & ML Orchestrator
===========================================

EdgeFlow is a modern, distributed platform for managing the entire lifecycle of data and machine learning (ML) workloads across a fleet of remote edge devices (IoT gateways, industrial PCs, etc.). It enables users to centrally define complex data transformations and inference pipelines as DAGs, and securely deploy them for localized, low-latency execution.

🚀 Key Features
----------------

EdgeFlow is built to handle the unique challenges of the computing continuum, where latency and network bandwidth are critical constraints.

🧠 Orchestration Layer (Centralized Control)
-------------------------

- **Pipeline-as-Code (DAGs):** Define entire data workflows (e.g., Sensor Ingestion -> Filtering -> Anomaly Detection) using configuration files (YAML/JSON).

- **Model Deployment & Synchronization:** Centralized management of ML artifacts (e.g., TFLite, ONNX models). Agents receive and load updated models over a secure gRPC channel.

- **Smart Placement Engine:** Future feature to intelligently decide which stage of the pipeline runs at the Edge and which runs in the Cloud based on resource metrics.

⚡ Data Streaming & Execution Layer (gRPC Core)
-------------------------

- **gRPC Bi-directional Streaming:** Uses gRPC/Protocol Buffers for highly efficient, strongly typed communication between Agents and the Central Server, minimizing network overhead and maximizing throughput.

- **Edge-Native Runtime:** The Edge Agent provides a lightweight runtime to load and execute Python functions for data transformation and ML inference locally.

- **Low-Latency Inference:** Deploying models directly on the edge allows for sub-millisecond inference times, critical for real-time control loops (e.g., robotics, quality control).

⚙️ Architecture & Dataflow Resilience
---

- **Event Sourcing:** Utilizes Kafka/Redis as a central event log for processed data, enabling temporal analysis and replaying of past events for debugging.

- **Local Caching for Models:** Agents cache ML models and pipeline definitions locally to maintain autonomous operation even during extended network disconnects.

- **Full Data Traceability:** Tracks data lineage from the source sensor to the final aggregated result in the cloud.


Folder Structure
---------

```aiignore
.
├── central-server/                 # The core orchestrator (FastAPI, Python)
│   ├── app/
│   │   ├── core/                   # ⬅️ NEW: Critical clients and logic
│   │   │   ├── mcp_client.py       # Manages communication with MCP Gateway (crucial!)
│   │   │   ├── ai_analyzer.py      # Placeholder for future LLM integration
│   │   │   └── exceptions.py       # Custom exception handling
│   │   ├── db/
│   │   │   ├── database.py         # DB connection setup (PostgreSQL)
│   │   │   └── crud.py             # CRUD functions for Node/Incident data
│   │   ├── models/                 # Pydantic & SQLAlchemy schemas
│   │   │   ├── node.py             # Node registration and status
│   │   │   └── incident.py         # Incident/Event log structure (New)
│   │   ├── routes/
│   │   │   ├── node_router.py      # Heartbeats, registration
│   │   │   └── data_router.py      # Telemetry ingestion, query APIs
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── edge-agent/                     # The telemetry and command executor (Python)
│   ├── core/
│   │   ├── collector.py            # Collects CPU/Mem/Logs (Metrics logic moves here)
│   │   ├── persistence.py          # ⬅️ NEW: Local caching for resilience
│   │   └── command_handler.py      # Executes commands pushed from Central Server
│   ├── agent.py                    # Main agent runner
│   └── Dockerfile
├── mcp-gateway/                    # ⬅️ NEW: Secure execution router
│   ├── gateway.py                  # Handles sessions, routing, and logging
│   ├── config/
│   │   └── catalog.yaml            # Tool definitions (who has what)
│   └── Dockerfile
├── mcp-servers/                    # ⬅️ NEW: Isolated tool execution modules
│   └── docker-control/             # The first tool server (Node.js/Python)
│       ├── server.js               # Tool logic (e.g., restart, get_logs)
│       └── package.json            # Dependencies for this server
└── infra/                          # Infrastructure files
    └── docker-compose.yaml         # Updated definition for all 5+ services
```