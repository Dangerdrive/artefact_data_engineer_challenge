# Deploying on Vercel

The project ships with an HTTP API so it can run as a **Vercel serverless
function** (ASGI). The same `Agent` used by the CLI serves the API.

## What is deployed

| File | Role |
|------|------|
| `src/api.py` | FastAPI app + `create_app()` factory |
| `api/index.py` | Vercel entrypoint that exports the ASGI `app` |
| `vercel.json` | Python runtime, `maxDuration`, bundled `src/` + `data/`, rewrites |
| `data/` | Self-contained copy of the CSVs + policies PDF (bundled for serverless) |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` (also `/health`, `/`) | Health + active mode |
| `POST` | `/api/chat` (also `/chat`, and a catch-all path) | Send a message |

Request:

```json
{ "message": "How much is the Takamine GD20?", "session_id": "cliente-42" }
```

Response:

```json
{ "reply": "The Takamine GD20 ... is R$ 2,199.00 ...", "mode": "llm", "session_id": "cliente-42" }
```

`session_id` is optional; it is used for best-effort in-memory conversation history.

## Steps

1. Push the repository to GitHub (must be public for the challenge).
2. In Vercel: **Add New → Project → Import** the repository.
3. Framework preset: **Other** (the `vercel.json` already configures the Python runtime).
4. Configure **Environment Variables** (Project Settings → Environment Variables):

   | Name | Value |
   |------|-------|
   | `LLM_PROVIDER` | `deepseek` |
   | `LLM_MODEL` | `deepseek-chat` |
   | `LLM_BASE_URL` | `https://api.deepseek.com` |
   | `LLM_API_KEY` | your DeepSeek key (mark as **Secret**) |
   | `LLM_TEMPERATURE` | `0.3` (optional) |
   | `LLM_MAX_TOKENS` | `512` (optional) |

   If `LLM_API_KEY` is not set, the API still works in **offline mode**.
5. Deploy. Use the deployment URL to test:

```bash
curl -s https://<your-project>.vercel.app/api/health

curl -s -X POST https://<your-project>.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"How much is the Takamine GD20?","session_id":"demo"}'
```

## Caveats (serverless)

- **Stateless by nature:** conversation history is kept in memory per warm instance
  and is **not guaranteed** across requests/cold starts. For durable history, store
  sessions in **Vercel KV / Upstash Redis**, or have the client send prior messages.
- **Cold starts:** the first request loads the CSVs and parses the policies PDF
  (fast, but not zero).
- **Timeouts:** `maxDuration` is set to 60s in `vercel.json`; actual limits depend on
  your Vercel plan. DeepSeek calls are usually fast.
- **Env vars only:** never commit `.env`; set secrets in the Vercel dashboard.
- **Data:** bundled from `data/` via `includeFiles`. If you change the dataset, update
  `data/` and redeploy.

## Local run (optional)

```bash
pip install uvicorn
uvicorn src.api:app --reload
# then open http://127.0.0.1:8000/docs
```
