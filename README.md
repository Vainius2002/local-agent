# PR Agent

A small FastAPI app that lets a logged-in user ask an OpenAI model to search, read, and write files, and to start, find, or kill local processes, through function calling. Built as a personal tool for driving local dev tasks (like restarting a service or reading a log) through plain language instead of a terminal.

## How it works

`/ask` renders a small chat page. Each question goes to the OpenAI Responses API (`gpt-5-mini`) along with a set of tools: `search_files`, `read_file`, `write_file`, `start_app`, `find_pid`, `kill_task`. The model decides if and when to call one, the app runs it locally, and the result goes back to the model until it has an answer for the user.

Typing `/convo` switches into a persistent conversation mode that keeps history between questions. `/stop` exits it.

## Authentication

This app has no login of its own. It delegates that to a separate service, [`auth`](https://github.com/Vainius2002/local-auth):

1. An unauthenticated request to `/ask` redirects to `auth`'s `/authorize`.
2. After logging in there, `auth` redirects back to this app's `/callback` with a one-time code.
3. `/callback` exchanges that code with `auth`'s `/token` endpoint for the user's identity, creates a local user record if needed, opens a session, and sets a cookie.

Both services need to be running for login to work.

## Setup

1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your own values.
4. `alembic upgrade head`
5. Generate a self-signed cert if you don't already have one: `openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes`
6. `uvicorn app.run:app --host 0.0.0.0 --port 8080 --ssl-keyfile=key.pem --ssl-certfile=cert.pem`

Browsers will flag the self-signed certificate as untrusted; that's expected for local use.

## Security note

The tools given to the model are intentionally unsandboxed: `read_file` and `write_file` can touch any file the host user can, and `find_pid`/`kill_task`/`start_app` can inspect or kill any process. This is meant for a single trusted user running it locally, never exposed to the internet or paired with an untrusted API key.
