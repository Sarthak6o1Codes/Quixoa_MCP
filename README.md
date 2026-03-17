# Quixoa MCP

Google Workspace MCP integration for LibreChat — Gmail, Drive, Calendar, Docs, Sheets, Forms, Tasks via AI.

---

## 1. Fork LibreChat

Fork: **https://github.com/danny-avila/LibreChat**

---

## 2. Add New Files

Copy these from this repo into your fork:

| Path | Purpose |
|------|---------|
| `Dockerfile.deploy` | Docker image (Node + Python) |
| `docker-compose.deploy.yml` | LibreChat + MongoDB + Meilisearch + OAuth |
| `docker-compose.google-workspace.yml` | Standalone MCP HTTP (optional) |
| `librechat.yaml` | MCP config for `google_workspace` |
| `scripts/google_auth_start.py` | OAuth entry point |
| `scripts/google_helper.py` | OAuth credentials & token storage |
| `scripts/mcp_server.py` | MCP server (Gmail, Drive, Calendar, etc.) |
| `scripts/gmail_tasks.py` | Gmail tools |
| `scripts/calendar_tasks.py` | Calendar tools |
| `scripts/calendar_detailed_tasks.py` | Calendar tools |
| `scripts/drive_tasks.py` | Drive tools |
| `scripts/drive_detailed_tasks.py` | Drive tools |
| `scripts/chat_tasks.py` | Google Chat tools |
| `scripts/editor_tasks.py` | Docs, Sheets, Slides tools |
| `scripts/task_tasks.py` | Google Tasks tools |
| `scripts/form_tasks.py` | Google Forms tools |
| `scripts/extra_tasks.py` | Search & other tools |
| `scripts/requirements.txt` | Python dependencies |
| `scripts/Dockerfile` | Standalone MCP image (optional) |
| `scripts/README_DOCKER.md` | MCP Docker usage |
| `GOOGLE_WORKSPACE_SETUP.md` | GCP OAuth setup |

---

## 3. Modify Existing Files

### `api/server/index.js`

Add the `/api/google-workspace/oauth/start` route (before middleware). It spawns the Python OAuth helper, reads the auth URL from stdout, and returns a 302 redirect to Google. Copy the route from this repo.

### `client/src/components/MCP/MCPServerMenuItem.tsx`

Add the "Sign in" link for `google_workspace` next to the server name (inside the server info div, when `server.serverName === 'google_workspace'`).

### `client/src/hooks/MCP/useMCPServerManager.ts`

Update `toggleServerSelection` for `google_workspace`: use anchor-based navigation to open the OAuth URL instead of `window.open`.

---

## 4. Requirements

- **Node.js** 20+ (LibreChat)
- **Python** 3.10+ with pip
- **Docker** & Docker Compose (for run)

### Python packages (for MCP)

```bash
pip install -r scripts/requirements.txt
```

Contents of `scripts/requirements.txt`:

```
google-api-python-client
google-auth-oauthlib
google-auth-httplib2
python-dotenv
pandas
mcp
```

---

## 5. Environment (.env)

Copy `.env.example` to `.env` and set:

### LLM API keys (required for chat)

At least one:

```env
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...
# or
GOOGLE_KEY=...          # Gemini API key
```

### Google Workspace MCP (required for Gmail, Drive, etc.)

```env
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
```

### GCP OAuth setup

1. [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
2. Create **OAuth 2.0 Client ID** (Web application)
3. Add **Authorized redirect URI**: `http://localhost:8080/`
4. Copy Client ID and Client secret into `.env`

### Optional

```env
GOOGLE_SEARCH_ID=...    # For web_search_internal tool
```

---

## 6. Run

```bash
docker compose -f docker-compose.deploy.yml up -d
```

Open **http://localhost:3080**

---

## 7. First Use

1. Sign up / log in to LibreChat
2. Create a chat
3. Open MCP servers menu, select **google_workspace**
4. Click **Sign in** → completes Google OAuth
5. Use Gmail, Drive, Calendar, Docs, Sheets, etc. in chat

---

See [GOOGLE_WORKSPACE_SETUP.md](GOOGLE_WORKSPACE_SETUP.md) for more OAuth details.

---

## 8. Cloud Run (optional)

To deploy to [Google Cloud Run](https://cloud.google.com/run):

### What’s integrated

- **LibreChat** + **Google Workspace MCP** (Gmail, Drive, Calendar, Docs, Sheets, Forms, Tasks)
- OAuth flow: `/api/google-workspace/oauth/start` → 302 redirect to Google → callback on port 8080
- MCP server runs as stdio child process (`scripts/mcp_server.py`)
- Token stored in `oauth_data/token.json`

### Deploy steps

1. **Build image**
   ```bash
   docker build -f Dockerfile.deploy -t gcr.io/YOUR_PROJECT_ID/quixoa-mcp .
   ```

2. **Push to Artifact Registry**
   ```bash
   docker push gcr.io/YOUR_PROJECT_ID/quixoa-mcp
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy quixoa-mcp \
     --image gcr.io/YOUR_PROJECT_ID/quixoa-mcp \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 3080
   ```

### Cloud Run notes

- **MongoDB & Meilisearch**: Use Cloud SQL / Atlas for MongoDB and a hosted Meilisearch (or similar) — Cloud Run runs only the app container.
- **OAuth callback**: The current flow uses a local Python server on port 8080. On Cloud Run you need a web-based callback route (e.g. `/api/google-workspace/oauth/callback`) instead of the local server. Add that route and set `GOOGLE_MCP_REDIRECT_URI` to your Cloud Run URL.
- **Secrets**: Use Secret Manager for `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and LLM API keys.
