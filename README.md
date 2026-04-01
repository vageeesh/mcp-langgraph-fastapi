# MCP Agentic Backend

A production-grade agentic backend built with **FastAPI**, **OpenAI Agents SDK**, and **Model Context Protocol (MCP)**.

## Architecture

```
Client → FastAPI (v1 API) → Agent Runner → MCP Server → Tools (SQL, Reporting)
                                  ↕                          ↕
                               Redis                     PostgreSQL
```

### Key Design Decisions

- **MCPServerStreamableHttp** — Production-standard communication layer using Streamable HTTP transport (HTTP + SSE). The MCP server runs as a standalone service, decoupled from the API server.

- **Dedicated MCP Server** — Runs as a separate Docker service (`mcp-server`), always available. The API server connects to it per-request via `async with`, keeping sessions lightweight and independent.

- **Agent Runner** — Separates agent orchestration from MCP connectivity. The runner connects the OpenAI Agent to the MCP server, streams responses back to the client, and manages conversation memory.

- **MCP Tools** — Tools (`execute_sql`, `get_reporting_schema`) are registered in the MCP server as separate modules. Adding new tools requires no changes to the agent or runner — just register them on the MCP server.

- **Streaming Responses** — Real-time token-by-token streaming from the agent to the client using `Runner.run_streamed()` and FastAPI's `StreamingResponse`.

- **Redis Conversation Memory** — Conversation history is stored in Redis per session, enabling multi-turn interactions. Configurable history depth via `MAX_HISTORY`.

- **API Versioning** — Routes are organized under `/api/v1/` for clean versioning and backward compatibility.

- **Data Visualization** — The agent automatically detects when data is best presented visually and returns structured visualization metadata. The Streamlit UI renders **line charts** (trends over time), **bar charts** (category comparisons), and **tables** (detailed listings) inline in the chat. No extra endpoints needed — visualization data flows through the same streaming response.

## Scalability

This architecture is horizontally scalable:

- **API Server** — Stateless. Scale by adding more instances behind a load balancer.
- **MCP Server** — Stateless per-request sessions. Scale independently of the API.
- **Redis** — Handles session memory. Can be clustered for high availability.
- **PostgreSQL** — The data layer. Supports read replicas and connection pooling.
- **Queue Integration** — Introduce a message queue (e.g., Redis Streams, RabbitMQ, Kafka) between the API and Agent Runner to handle millions of concurrent users with backpressure and retry logic.

## Project Structure

```
app/
├── main.py                 # FastAPI app entry point
├── routers.py              # Top-level router aggregation
├── api/v1/router.py        # Versioned API routes
├── agents/sql_agent.py     # Agent definition and system prompt
├── agents_runner/runner.py # MCP connection + streaming orchestration
├── core/
│   ├── config.py           # Settings (env-based)
│   ├── database.py         # PostgreSQL connection
│   ├── redis.py            # Redis client for conversation memory
│   └── tools/sql_tool.py   # SQL execution tool
├── modules/reporting/      # Reporting module (models, schemas, services)
mcp_server/
├── server.py               # Standalone MCP server (FastMCP + Streamable HTTP)
```

## Running

```bash
docker-compose up --build
```

Services:
- **API**: `http://localhost:8000`
- **MCP Server**: `http://localhost:8001`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

## Environment Variables

See `env.example` for required configuration:
- `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL`
- `POSTGRES_*` — Database connection
- `REDIS_HOST` / `REDIS_PORT` — Redis connection
- `MCP_SERVER_URL` — MCP server endpoint
- `MAX_HISTORY` — Number of conversation turns to retain
