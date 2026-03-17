# Google Workspace MCP - Docker

Standalone HTTP endpoint for the Google Workspace MCP server.

## Build

```bash
docker build -f scripts/Dockerfile -t google-workspace-mcp .
```

## Run

```bash
docker run -d -p 8000:8000 \
  -e GOOGLE_CLIENT_ID=your_client_id \
  -e GOOGLE_CLIENT_SECRET=your_client_secret \
  --name google-workspace-mcp google-workspace-mcp
```

Or with docker-compose:

```bash
docker compose -f docker-compose.google-workspace.yml up -d
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check – returns `{"status":"ok","service":"google-workspace-mcp"}` |
| `POST /mcp` | MCP Streamable HTTP protocol (for LibreChat / MCP clients) |

## Test

```bash
# Health check
curl http://localhost:8000/health
```

## Env vars

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_CLIENT_ID` | Yes | GCP OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Yes | GCP OAuth client secret |
| `MCP_TRANSPORT` | No | Set to `http` for HTTP mode (default in Docker) |
| `MCP_PORT` | No | Port (default: 8000) |
