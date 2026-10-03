# conftest.py — shared pytest fixtures for RAAHAT integration tests

import pytest
import requests

BASE = "http://localhost:8000"


@pytest.fixture(scope="session", autouse=True)
def check_backend_running():
    """Fail fast if backend is not reachable before any test runs."""
    try:
        r = requests.get(f"{BASE}/health", timeout=5)
        r.raise_for_status()
    except Exception:
        pytest.exit(
            f"\n[RAAHAT] Backend not reachable at {BASE}.\n"
            "Start it with:  uvicorn app.main:app --reload --port 8000\n",
            returncode=1,
        )
