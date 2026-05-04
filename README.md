CSCI 5300 Software Engineering Project

# Melody Matrix 🎵

**Music Generator** — A web application for generating music, with Supabase authentication and a FastAPI-backed chat assistant.

## Overview

Melody Matrix is a web app that combines static pages (login, signup, dashboard, generation flows) with a Python backend. Users sign in via Supabase; the dashboard and related pages talk to local APIs when served over HTTP (not `file://`).

## Features

### Frontend (`frontend/public/`)

- **Login** (`login.html`) — Email/password, Google OAuth, guest login, validation, link to signup.
- **Signup** (`index.html`) — Registration, password confirmation, Google OAuth, email verification support.
- **Dashboard** (`dashboard.html`) — Music / Markov-style controls and session UX.
- **Generate** (`generate.html`), **saved outputs**, **settings**, **guest**, **reset-password** — Supporting flows and UI.
- **Chatbot** — Client script (`chatbot.js`) calling the FastAPI `/api/chat` endpoint.
- **Design** — Pastel palette, floating music notes, responsive layout, Poppins, transitions.

### Backend (`backend/`)

- **FastAPI** (`main.py`) — Chat API and health check; started by `start.py` on port **5001** via Uvicorn.
- **Flask** (`app.py`, `routes.py`, `guest_routes.py`, etc.) — Additional routes and music tooling used in development; see code for entrypoints.

### Optional

- **Ollama** (local, port `11434`) — Improves chatbot answers when running; otherwise the app uses built-in fallbacks.

## Security

**IMPORTANT:** Put Supabase credentials only in `frontend/public/config.js`. Do not commit real keys. Use `frontend/public/config.example.js` as a template. Treat `config.js` like a secret (keep it out of Git and shared drives you do not trust).

## Getting started

### Prerequisites

- **Python 3** with the `python3` command available in your terminal (macOS/Linux: default; see **Windows** below).
- A modern browser.
- A **Supabase** project ([supabase.com](https://supabase.com)) for auth.
- Optional: **Ollama** for richer chatbot responses.

### 1. Clone the repository

```bash
git clone <repository-url>
cd MelodyMatrix
```

(Use your actual folder name if it differs.)

### 2. Supabase setup

1. Create a project in the Supabase dashboard.
2. **Settings → API** — copy the **Project URL** and **anon public** key.

### 3. Create `config.js`

From the repo root:

```bash
cp frontend/public/config.example.js frontend/public/config.js
```

Edit `frontend/public/config.js` and set your Supabase URL and anon key (same shape as in the example file).

### 4. Python dependencies

The launcher starts **Uvicorn** + **FastAPI**. Install packages into the same Python that runs `python3`:

```bash
python3 -m pip install -r backend/requirements.txt
```

(`backend/requirements.txt` includes Flask/music libs plus **FastAPI**, **Uvicorn**, **requests**, and **pydantic** for the chat API.)

### Docker (consistent environment)

From the repo root:

```bash
docker compose up --build
```

- Frontend: `http://localhost:8000/login.html`
- API health: `http://localhost:5001/api/health`

Copy `frontend/public/config.example.js` to `frontend/public/config.js` on your machine for Supabase auth (same as non-Docker runs).

### CI

GitHub Actions runs on pushes and PRs to `main` / `master` (and `feature/**` branches on push): Python compile/import checks and a **Docker Compose** build + smoke test. See `.github/workflows/ci.yml`.

### 5. Run the application

From the **repository root** (where `start.py` lives):

```bash
python3 start.py
```

This will:

- Start the FastAPI app on **http://127.0.0.1:5001**
- Serve the static site from `frontend/public` on **http://127.0.0.1:8000**
- Open the login page in your browser

Useful URLs:

- `http://127.0.0.1:8000/login.html`
- `http://127.0.0.1:8000/index.html` (signup)
- `http://127.0.0.1:8000/dashboard.html`

Stop the stack with **Ctrl+C** in the terminal.

#### Manual run (two terminals)

```bash
# Terminal 1 — API
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 5001

# Terminal 2 — static files
cd frontend/public
python3 -m http.server 8000
```

Then open `http://127.0.0.1:8000/login.html`.

### Windows: `python3` and “Microsoft Store” message

`start.py` invokes **`python3`**. If Windows shows “Python was not found… Microsoft Store”:

1. **Settings → Apps → App execution aliases** — turn **off** aliases for `python.exe` / `python3.exe` that point to the Store.
2. Install Python from [python.org](https://www.python.org/downloads/windows/) and enable **Add to PATH**.
3. Open a **new** terminal and run `python3 --version`, then install deps with `python3 -m pip install ...` as above.

Alternatively, use **WSL2 (Ubuntu)** and follow the same `python3` commands as on macOS.

### Google OAuth (optional)

1. **Google Cloud Console** — OAuth client (Web). Authorized JavaScript origins: `http://127.0.0.1:8000` and/or `http://localhost:8000`. Redirect URI: `https://<your-project-ref>.supabase.co/auth/v1/callback`.
2. **Supabase → Authentication → Providers → Google** — enable and paste client ID/secret.
3. **Supabase → Authentication → URL Configuration** — set **Site URL** and **Redirect URLs** to match how you open the app (include exact paths such as `/login.html`, `/index.html`, `/dashboard.html` if required by your Supabase settings).

### Supabase auth settings

- Enable **Email** under Authentication → Providers for password sign-in.
- Optionally enable **Anonymous** for true guest sessions (otherwise guest mode may use local fallbacks).

## Project structure

```
MelodyMatrix/
├── start.py                 # Starts FastAPI (5001) + http.server for frontend/public (8000)
├── README.md
├── supabase/
│   └── migrations/          # SQL migrations (e.g. helper functions)
├── frontend/
│   ├── public/              # Static HTML, CSS, JS, config.example.js, config.js (local only)
│   └── src/                 # Additional frontend source (e.g. App.jsx)
├── backend/
│   ├── main.py              # FastAPI app (chat, health)
│   ├── app.py               # Flask app (alternate / extended server)
│   ├── routes.py            # Flask API and page routes
│   ├── chatbot.py           # Chat logic / Ollama integration
│   ├── music_generator.py   # Generation helpers
│   ├── guest_routes.py      # Guest-related Flask blueprint
│   ├── requirements.txt     # Python dependencies (install FastAPI stack separately as above)
│   └── ...
└── data/                    # Shared data / scripts (e.g. MIDI tooling)
```

## Authentication flow (summary)

1. **Email/password signup** — `index.html` → Supabase sign-up → optional email verification → login on `login.html`.
2. **Email/password login** — `login.html` → session stored in the browser (localStorage) as implemented in the pages.
3. **Google** — OAuth via Supabase; returning users are recognized by Supabase.
4. **Guest** — Anonymous provider or local guest fallback depending on Supabase settings.

## Configuration notes

- **config path:** `frontend/public/config.js` (must sit next to the HTML that loads it).
- **Password rules:** Minimum length and confirm-password checks are enforced in the signup UI (see project code for exact rules).
- **localStorage:** Used for session and UI state as documented in individual pages.

## Troubleshooting

| Issue | What to try |
|--------|-------------|
| **Backend failed to start** | Run `cd backend && python3 -m uvicorn main:app --port 5001` manually to see errors. Install `fastapi`, `uvicorn`, `requests` with the same `python3`. Ensure port **5001** is free. |
| **`python3` not found (Windows)** | Disable Store app aliases; install python.org Python; or use WSL. |
| **Auth / “configuration missing”** | Ensure `frontend/public/config.js` exists and defines the same `CONFIG` keys as `config.example.js`. |
| **OAuth / redirect errors** | Supabase **Redirect URLs** and Google **authorized origins** must match the URL you use (`127.0.0.1` vs `localhost` are different hosts). |
| **Chatbot weak answers** | Start [Ollama](https://ollama.com) on port 11434 or rely on built-in fallbacks. |

## Future development

- [ ] Extended music generation and export flows
- [ ] User profile management
- [ ] Deeper session management
- [ ] Hardening and tests across Flask/FastAPI boundaries

---

*This README reflects the current layout with `frontend/public` and `start.py`. If you add new services or change ports, update the run instructions and Supabase URL settings to match.*
