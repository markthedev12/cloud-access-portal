# CloudAccess Portal

An early Python/FastAPI backend for an access-request portal. The current
implementation provides health endpoints and validated user registration backed
by SQLAlchemy. Access approval, authentication, a frontend, AI assistance, and
AWS provisioning are roadmap items—not implemented features.

## Run locally

Requires Python 3.12+. From the repository root:

```sh
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m backend.init_db
python -m uvicorn backend.main:app --reload --host 127.0.0.1
```

Open http://127.0.0.1:8000/docs for the interactive API. `GET /health` is a
process health check, not a database readiness test. `POST /users/` accepts an
email, a password of 12–128 characters, and optional full name. It returns public
user fields with HTTP 201, rejects invalid inputs with 422, and duplicates with
400. Try only fictional data. There is no login or session endpoint yet.

Default storage is `portal.db` in the working directory. Set `DATABASE_URL`
using `.env.example` as a guide. A non-SQLite backend needs its own driver and
configuration; PostgreSQL deployment has not been implemented here.

### Optional Docker development

```sh
docker compose up --build
docker compose down
```

The container initializes a local SQLite volume and binds the API to host
loopback. `docker compose down --volumes` discards that demo database. The
Dockerfile is a development convenience, not a reviewed production deployment.

## Architecture and decisions

`HTTP request -> Pydantic validation -> FastAPI route -> SQLAlchemy -> SQLite`

`backend/security.py` hashes new passwords with salted Argon2 through pwdlib.
The response schema excludes hashes. Database uniqueness protects email records
and the route rolls back conflicting writes. Password hashing follows the
[FastAPI password-hashing guide](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
Earlier SHA-256 hashes are not upgraded automatically; reset fictional local
accounts. Real stored accounts would need a separate migration/reset plan.

## Verify

```sh
python -m unittest discover -s tests -v
```

Tests override the database with an isolated in-memory SQLite instance and cover
registration, duplicates, invalid input, salted hashes, wrong-password rejection,
and password-free responses. CI runs Python 3.12/3.13. No AWS access is needed.

## Scope and next milestones

- Add migrations and a managed identity or complete session design.
- Model requests, reviewers, expiry and append-only decision events.
- Enforce ownership and prevent self-approval on the server.
- Add a Next.js UI and a complete request/review browser test.
- Add policy-grounded AI explanations behind a provider interface; AI must not grant access.
- Deploy only after cost review, least-privilege IAM, secrets, TLS and monitoring.

Registration is currently unauthenticated and lacks abuse controls. Do not expose
this prototype publicly or store employer/patient data. No compliance guarantee
is implied. Contributions should keep handlers small and add API tests for
behavior changes. Repository map: `backend/`, `tests/`, dependency files, and
optional Docker development configuration.
