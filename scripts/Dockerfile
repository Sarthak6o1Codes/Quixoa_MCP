# Google Workspace MCP - HTTP endpoint for LibreChat
# Build: docker build -f scripts/Dockerfile -t google-workspace-mcp .
# Run:  docker run -p 8000:8000 -e GOOGLE_CLIENT_ID=... -e GOOGLE_CLIENT_SECRET=... google-workspace-mcp

FROM python:3.12-slim

WORKDIR /app

# Copy scripts (context: LibreChat root when using -f scripts/Dockerfile .)
COPY scripts/ ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run MCP server in HTTP mode
ENV MCP_TRANSPORT=http
ENV MCP_PORT=8000

EXPOSE 8000

CMD ["python", "mcp_server.py"]
