# Pastebin-Lite

A minimal Pastebin-like web application that allows users to create text pastes and share links to view them.  
Each paste can optionally expire based on **time-to-live (TTL)** and/or **maximum view count**.

This project was built as part of a take-home assignment and is designed to pass automated API and behavior tests.

---

##  Live Demo

**Deployed URL:** (URL shows resource is not currently available because debug mode on in production) - but when you hit exact end points, it gives results.  
https://pastebin-5xm7.onrender.com

---

##  Features

- Create a text paste via API
- Generate a shareable URL
- View pastes as:
  - JSON (API)
  - HTML (browser)
- Optional constraints:
  - Time-based expiry (TTL)
  - View-count limit
- Deterministic time handling for automated testing
- Safe HTML rendering (no script execution)
- Persistent storage (no in-memory state)

---

##  Tech Stack

- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL (Render-managed)
- **Deployment:** Render
- **Testing:** Django `unittest` (`Django TestCase`)

---

##  Persistence Layer

This application uses **PostgreSQL** as the persistence layer.

- The database is managed by **Render**
- Data survives across requests and restarts
- No in-memory storage is used for paste data

---

## API Endpoints

### Health Check

**GET** `/api/healthz`

Returns HTTP `200` and JSON.  
Verifies database connectivity.

**Example response:**
```json
{ "ok": true }

```
Create a Paste
POST /api/pastes

Request body (JSON):

```json
{
  "content": "Hello world",
  "ttl_seconds": 60,
  "max_views": 5
}
```
Rules:

content is required and must be a non-empty string

ttl_seconds (optional) must be an integer ≥ 1

max_views (optional) must be an integer ≥ 1

Successful response (201):

```json
Copy code
{
  "id": "be010435-dcde-4ac1-b1b7-9a8aeef06dcd",
  "url": "https://pastebin-5xm7.onrender.com/p/be010435-dcde-4ac1-b1b7-9a8aeef06dcd"
}
```
Fetch a Paste (API)
GET /api/pastes/:id

Successful response (200):

```json
Copy code
{
  "content": "Hello world",
  "remaining_views": 4,
  "expires_at": "2026-01-01T00:00:00Z"
}
```
Notes:

remaining_views is null if unlimited

expires_at is null if no TTL

Each successful fetch counts as a view

Expired, view-limited, or missing pastes return HTTP 404 with JSON

View a Paste (HTML)
GET /p/:id

Returns HTML containing the paste content

Content is rendered safely (no script execution)

Returns HTTP 404 if the paste is unavailable

## Deterministic Time Support (Testing)
For automated testing, deterministic expiry behavior is supported.

If the environment variable is set:


TEST_MODE=1

Then the request header:

x-test-now-ms: <milliseconds since epoch>
Is treated as the current time for expiry logic only

If the header is absent, real system time is used

##  Testing

The project includes unit tests written using Django’s built-in unittest framework.

Covered scenarios:

Health check

Paste creation (valid & invalid input)

Fetching pastes via API

HTML paste rendering

TTL expiry

View-count limits

Combined TTL + max views behavior

## Run tests locally:

```
python manage.py test
```

##  Running Locally

Prerequisites
Python 3.10+

PostgreSQL

Virtual environment (recommended)

Setup
```
git clone <your-repo-url>
cd pastebin_lite
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Environment Variables
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@host:port/dbname
TEST_MODE=1   # optional (used only for deterministic testing)
```
Run Migrations and Start Server

```
python manage.py migrate
python manage.py runserver
```

##  Environment Variables (Production)
The following environment variables are required:

SECRET_KEY – Django secret key

DATABASE_URL – PostgreSQL connection string

TEST_MODE – Optional; enables deterministic time handling

Environment variables are configured on the deployment platform and are not committed to the repository.

##   Design Notes
Uses database transactions and row locking to safely enforce TTL and view limits under concurrent access

Avoids global mutable state (safe for serverless environments)

Returns consistent JSON responses for all API errors

Keeps routing modular using app-level URLs
