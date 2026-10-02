# Raahat
AI-Powered Disaster Response and Resource Coordination Platform for Low-Connectivity Environments

## Backend

FastAPI app in backend/. Needs Python 3.10 or newer.

cd backend
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/uvicorn app.main:app --reload

The API runs on http://127.0.0.1:8000, interactive docs at /docs.

- POST /simulate/sms stores a fake inbound SMS as a ticket
- GET /requests returns all tickets, newest first
- PATCH /requests/{id} sets category, urgency or status

Tests: cd backend && ./.venv/bin/python -m pytest
