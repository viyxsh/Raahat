import os
import tempfile

_tmp = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = "sqlite:///" + _tmp + "/test.db"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SAMPLE = {
    "message": "NEED WATER SECTOR 3",
    "phone": "+911234567890",
    "lat": 23.21,
    "lng": 77.41,
}


def test_simulate_sms_creates_ticket():
    resp = client.post("/simulate/sms", json=SAMPLE)
    assert resp.status_code == 201
    ticket = resp.json()
    assert ticket["text"] == "NEED WATER SECTOR 3"
    assert ticket["status"] == "new"
    # the classifier runs at intake: water keywords set the category
    assert ticket["category"] == "water"
    assert ticket["urgency"] in ("low", "medium", "high", "critical")
    assert ticket["created_at"]


def test_list_requests_wraps_tickets():
    client.post("/simulate/sms", json=SAMPLE)
    resp = client.get("/requests")
    assert resp.status_code == 200
    body = resp.json()
    assert set(body.keys()) == {"tickets"}
    assert len(body["tickets"]) >= 1


def test_patch_updates_status():
    created = client.post("/simulate/sms", json=SAMPLE).json()
    resp = client.patch("/requests/" + str(created["id"]), json={"status": "verified"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "verified"


def test_patch_rejects_unknown_status():
    created = client.post("/simulate/sms", json=SAMPLE).json()
    resp = client.patch("/requests/" + str(created["id"]), json={"status": "done"})
    assert resp.status_code == 422


def test_patch_rejects_null_status():
    created = client.post("/simulate/sms", json=SAMPLE).json()
    resp = client.patch("/requests/" + str(created["id"]), json={"status": None})
    assert resp.status_code == 422


def test_patch_without_status_keeps_partial_update():
    created = client.post(
        "/simulate/sms", json=dict(SAMPLE, message="FIELD CHECK UNIQUE TICKET")
    ).json()
    resp = client.patch("/requests/" + str(created["id"]), json={"urgency": "low"})
    assert resp.status_code == 200
    assert resp.json()["urgency"] == "low"
    # PATCH must not resurrect a flagged ticket to new; it leaves status alone
    assert resp.json()["status"] == created["status"]


def test_rejects_out_of_range_location():
    bad = dict(SAMPLE, lat=999)
    assert client.post("/simulate/sms", json=bad).status_code == 422


def test_missing_ticket_returns_404():
    assert client.get("/requests/9999").status_code == 404
