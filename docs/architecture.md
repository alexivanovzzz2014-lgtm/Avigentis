# Architecture

- Frontend captures lead form and displays preliminary summaries.
- FastAPI API validates domain-only input, applies rate limits, stores scans, and secures admin views.
- Scanner engine runs only public signal checks (HTTPS, headers, DNS, policy signals).
- Scoring is transparent and centralized in `backend/app/services/scoring.py`.
- Summaries produce public and internal expert narratives with safe disclaimers.
