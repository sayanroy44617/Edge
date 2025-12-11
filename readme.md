🤖 SRE Sentinel: AI-Powered Self-Healing Orchestrator
---

SRE Sentinel is an autonomous infrastructure platform that closes the loop between monitoring and remediation.

Unlike traditional monitoring tools that just alert you when something breaks, SRE Sentinel uses an AI Analyzer to determine the root cause and securely executes fixes via the Model Context Protocol (MCP).

🚀 Key Features

- Real-time Monitoring: Distributed Edge Agents push telemetry (CPU, Memory, Disk) to a centralized brain.

- AI-Driven Root Cause Analysis (RCA): Automatically analyzes anomalies using LLMs to distinguish between transient spikes and actual failures.

- Secure Remediation (MCP): Uses the Model Context Protocol to execute infrastructure commands (like docker restart) in a sandboxed, auditable environment.

- Resilient Architecture: Agents cache data locally during network outages and sync when online.

🏗️ Architecture

The system is composed of three distinct layers:

- Edge Layer (edge-agent): Lightweight Python agents running on Docker hosts. They collect metrics and listen for commands.

- Central Intelligence (central-server): A FastAPI orchestrator backed by PostgreSQL (State) and Redis (Event Bus). It ingests heartbeats and triggers the AI analysis.

- Execution Layer (mcp-gateway & mcp-servers): A secure gateway that routes approved "Fix Actions" to isolated tool servers, ensuring the AI never has direct root access.

🛠️ Tech Stack

- Backend: FastAPI (Python 3.11), Pydantic V2

- Database: PostgreSQL 15, SQLAlchemy (ORM)

- Caching/Queues: Redis 7

- Infrastructure: Docker & Docker Compose

Protocol: Model Context Protocol (MCP) for tool execution

📂 Project Structure

```
.
├── central-server/         # The Brain (FastAPI + DB)
│   ├── app/
│   │   ├── core/           # Config & MCP Client
│   │   ├── db/             # Database connection & CRUD
│   │   ├── models/         # SQLAlchemy Tables (Nodes, Incidents)
│   │   ├── schemas/        # Pydantic Models (Base/Create/Read)
│   │   └── routes/         # API Endpoints
│   └── Dockerfile
├── edge-agent/             # The Observer (Collector)
│   ├── core/               # Telemetry logic & Local Cache
│   └── agent.py
├── mcp-gateway/            # The Secure Router
│   └── config/catalog.yaml # Tool definitions
├── infra/                  # Infrastructure Configuration
│   └── docker-compose.yaml # Service orchestration
└── requirements.txt
```


⚡ Getting Started

Prerequisites

- Docker & Docker Compose

- Python 3.10+ (for local development)

1. Configuration

Create a .env file in the central-server directory:

```
POSTGRES_USER=edgectrl_user
POSTGRES_PASSWORD=edgectrl_password
POSTGRES_DB=edgectrl_db
POSTGRES_HOST=postgres
```


2. Run the Stack

We use Docker Compose to spin up the Database, Central Server, and Cache.

# Start all services
docker-compose -f infra/docker-compose.yaml up -d --build

# Check logs to ensure DB tables are created
docker-compose -f infra/docker-compose.yaml logs -f central-server


3. Verify Health

Once running, visit the API documentation:

Swagger UI: http://localhost:8000/docs

Health Check: GET http://localhost:8000/

🛣️ Roadmap

[x] Phase 1: Foundation (DB, Models, Schemas, Infrastructure)

[ ] Phase 2: Monitoring Loop (Agent Heartbeat API, CRUD implementation)

[ ] Phase 3: Intelligence (LLM Integration for Anomaly Detection)

[ ] Phase 4: Execution (MCP Gateway & Docker Control Server)

🤝 Contributing

Fork the repository.

Create a feature branch (git checkout -b feature/amazing-feature).

Commit your changes (git commit -m 'Add some amazing feature').

Push to the branch (git push origin feature/amazing-feature).

Open a Pull Request.
