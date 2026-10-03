# RAAHAT — Task 5: Integration & Demo
## Owner: [Your Name]

This folder contains everything needed to wire, seed, test, and demonstrate
the RAAHAT system end-to-end.

---

## Quick Start

### 1. Install demo dependencies
```bash
pip install -r demo/requirements.txt
```

### 2. Start the backend (Diya's task)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Start the frontend (Vinit + Manvi's task)
```bash
cd frontend
npm install
npm run dev
```

### 4. Seed the demo data (20 tickets)
```bash
python demo/run_demo.py
# Options:
#   --base http://localhost:8000    (custom backend URL)
#   --delay 0.5                    (seconds between requests)
#   --ticket 17,18                 (fire specific tickets only)
```

### 5. Run integration tests
```bash
pytest demo/integration_tests/ -v
```

### 6. (Optional) Set up ngrok for reviewer access
```bash
# See demo/ngrok_setup.md for full instructions
ngrok http 8000
python demo/run_demo.py --base https://YOUR_NGROK_URL.ngrok-free.app
```

---

## File Structure

```
demo/
├── test_data.json              ← 20 realistic test tickets
├── run_demo.py                 ← Seeds all tickets + shows results
├── demo_script.md              ← Presenter's word-for-word guide (8 scenes)
├── ngrok_setup.md              ← Step-by-step ngrok tunnel instructions
├── requirements.txt            ← pip install -r this before running anything
├── integration_tests/
│   ├── conftest.py             ← Backend health check fixture
│   └── test_api_contract.py   ← 21 integration tests
└── screenshots/                ← Capture here for report Ch 5
```

---

## What This Covers (Task 5 Deliverables)

| Deliverable | File | Status |
|-------------|------|--------|
| Test data (20 tickets) | `test_data.json` | ✅ Done |
| Auto-seeder script | `run_demo.py` | ✅ Done |
| Integration tests | `integration_tests/` | ✅ Done |
| ngrok setup guide | `ngrok_setup.md` | ✅ Done |
| Demo presenter script | `demo_script.md` | ✅ Done |
| Report Ch 1 (Introduction) | `docs/report/ch1_introduction.md` | ✅ Done |
| Report Ch 4 (Results) | `docs/report/ch4_results_discussion.md` | ✅ Done |
| Report Ch 5 (Conclusion) | `docs/report/ch5_conclusion.md` | ✅ Done |
| PPT slides (6 slides) | `docs/ppt/task5_slides_content.md` | ✅ Done |

---

## API Contract (reference)

```
POST /simulate/sms
Body: { "message": str, "phone": str, "lat": float, "lng": float }
Returns 201: { id, text, phone, lat, lng, category, urgency, status, created_at }

GET /requests
Returns 200: { "tickets": [ ...TicketOut ] }   ← sorted critical→low
```
