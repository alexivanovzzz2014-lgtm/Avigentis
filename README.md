# Avigentis Cyber Readiness Scanner (MVP)

MVP SaaS platform for preliminary NIS2 / ЗКС readiness analysis based only on publicly accessible information.

## Disclaimer
"Скенерът анализира само публично достъпна информация. Резултатът е предварителен и не представлява официален одит, правно становище или гаранция за съответствие."

Avigentis is a consultant and provides support for achieving compliance; it is not a guarantor of compliance.

## Stack
- Frontend: Next.js + TypeScript + Tailwind
- Backend: FastAPI + SQLAlchemy + Pydantic
- DB: PostgreSQL
- Queue: Celery + Redis
- Auth: MVP admin email/password + JWT

## Structure
- `frontend/`
- `backend/`
- `docker/`
- `docs/`

## Local run
1. `cp .env.example .env`
2. `docker compose up --build`
3. Frontend: `http://localhost:3000`
4. Backend docs: `http://localhost:8000/docs`

## Backend direct run
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Example API requests
```bash
curl -X POST http://localhost:8000/api/scans -H 'Content-Type: application/json' -d '{"domain":"example.bg","email":"test@example.bg","gdpr_consent":true,"public_info_acknowledgment":true,"organization_type":"Municipality"}'
curl -X POST http://localhost:8000/api/auth/login -H 'Content-Type: application/json' -d '{"email":"admin@avigentis.bg","password":"admin123"}'
```

## Tests
```bash
cd backend
pytest -q
```

## TODO (production hardening)
- Persistent distributed rate limiting (Redis token bucket)
- Strong admin auth (MFA + user table)
- Background job orchestration for scans
- Better SSRF hardening with allow/deny lists and DNS rebinding defenses
- Structured logging/monitoring and audit trails
- Expand DKIM detection strategies and false positive controls
