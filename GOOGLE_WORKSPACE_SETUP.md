# Google Workspace MCP Integration Setup

This LibreChat instance includes the **Google Workspace MCP** integration. When users click the **google_workspace** MCP server in the chat menu, an OAuth popup opens so they can sign in and use Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Tasks, Chat, and more.

---

## Required .env Variables

Add these to your `.env` file (copy from `.env.example` if needed):

```env
# ===========================================
# Google Workspace MCP (required for MCP tools)
# ===========================================
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# Optional: Custom OAuth redirect (default: http://localhost:8080/, must match Docker port mapping)
# GOOGLE_MCP_REDIRECT_URI=http://localhost:8080/
```

**Note:** `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are shared with LibreChat's built-in Google social login. If you already use "Sign in with Google", you can reuse the same credentials.

---

## GCP OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → **Credentials**.
2. Create an **OAuth 2.0 Client ID** (Web application).
3. Add these **Authorized redirect URIs**:
   - `http://localhost:8080/` — for MCP OAuth (required)
   - `http://localhost:3080/oauth/google/callback` — for LibreChat social login (optional)
4. Copy the **Client ID** and **Client secret** into your `.env` file.

---

## Optional: Google Custom Search

For the `web_search_internal` tool:

```env
GOOGLE_SEARCH_ID=your_cse_id
```

---

## Python Dependencies

Install the Python packages for the MCP server:

```bash
cd LibreChat
pip install -r scripts/requirements.txt
```

---

## Flow

1. User clicks **google_workspace** in the MCP servers menu.
2. OAuth popup opens at `/api/google-workspace/oauth/start`.
3. A Python script starts a local server on port 8080 for the callback.
4. User signs in with Google and grants permissions.
5. `token.json` is saved in the LibreChat root.
6. User can use Gmail, Drive, Calendar, Docs, Sheets, etc. from the chat.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `python: command not found` | Use `python3` in `librechat.yaml` on Linux/Mac, or ensure `python` is in PATH on Windows. |
| Port 8080 in use | Ensure no other service uses 8080; OAuth callback needs it. |
| OAuth popup blocked | Allow popups for your LibreChat domain. |
| `token.json` not found | Run OAuth again; ensure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set. |
