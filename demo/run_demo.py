"""
RAAHAT Demo Seeder -- run_demo.py
Task 5: Integration & Demo Scenarios

Usage:
    python demo/run_demo.py                   # fires all 20 tickets sequentially
    python demo/run_demo.py --base http://... # custom backend URL
    python demo/run_demo.py --delay 0.5      # seconds between requests (default 0.5)
    python demo/run_demo.py --ticket 17,18   # fire specific ticket numbers only
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Force UTF-8 output on Windows so the terminal doesn't crash on special chars
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("[ERROR] 'requests' library not installed. Run: pip install requests")
    sys.exit(1)

# ── colour helpers (Windows-safe) ────────────────────────────────────────────
try:
    import colorama
    colorama.init(autoreset=True)
    RED    = "\033[91m"
    ORANGE = "\033[93m"
    YELLOW = "\033[33m"
    GREEN  = "\033[92m"
    CYAN   = "\033[96m"
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
except ImportError:
    RED = ORANGE = YELLOW = GREEN = CYAN = RESET = BOLD = ""

URGENCY_COLOUR = {
    "critical": RED,
    "high":     ORANGE,
    "medium":   YELLOW,
    "low":      GREEN,
}

STATUS_COLOUR = {
    "new":      CYAN,
    "flagged":  ORANGE,
    "verified": GREEN,
    "assigned": "\033[35m",
}

# ── helpers ───────────────────────────────────────────────────────────────────

def print_banner():
    print(f"\n{BOLD}{'='*65}")
    print("   RAAHAT — Demo Seeder  |  Task 5: Integration & Demo")
    print(f"{'='*65}{RESET}\n")


def fire_ticket(base: str, payload: dict, idx: int, expected: dict) -> dict | None:
    """POST /simulate/sms and return the created ticket or None on failure."""
    try:
        r = requests.post(
            f"{base}/simulate/sms",
            json=payload,
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        print(f"  [{idx:02d}] {RED}CONNECTION ERROR — is the backend running at {base}?{RESET}")
        return None
    except requests.exceptions.HTTPError as exc:
        print(f"  [{idx:02d}] {RED}HTTP {exc.response.status_code}{RESET}")
        return None
    except Exception as exc:
        print(f"  [{idx:02d}] {RED}ERROR: {exc}{RESET}")
        return None


def check_expectation(data: dict, expected: dict) -> str:
    """Return '✅' if category + urgency + status match expected values."""
    mismatches = []
    for field in ("category", "urgency", "status"):
        exp = expected.get(f"expected_{field}")
        got = data.get(field)
        if exp and got != exp:
            mismatches.append(f"{field}: got '{got}' expected '{exp}'")
    if mismatches:
        return f"[!!] {', '.join(mismatches)}"
    return "[OK]"


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="RAAHAT Demo Seeder")
    parser.add_argument("--base",   default="http://localhost:8000", help="Backend base URL")
    parser.add_argument("--delay",  type=float, default=0.5,         help="Delay between requests (s)")
    parser.add_argument("--ticket", default="",                       help="Comma-separated ticket numbers to fire (1-indexed)")
    args = parser.parse_args()

    base = args.base.rstrip("/")

    # Load test data
    data_path = Path(__file__).parent / "test_data.json"
    if not data_path.exists():
        print(f"[ERROR] test_data.json not found at {data_path}")
        sys.exit(1)
    with open(data_path, encoding="utf-8") as f:
        all_tickets = json.load(f)

    # Filter if --ticket specified
    if args.ticket:
        indices = [int(x.strip()) - 1 for x in args.ticket.split(",")]
        tickets = [(i, all_tickets[i]) for i in indices if 0 <= i < len(all_tickets)]
    else:
        tickets = list(enumerate(all_tickets))

    print_banner()

    # Health check
    try:
        hc = requests.get(f"{base}/health", timeout=5)
        print(f"  Backend {GREEN}online{RESET} at {base}  (status {hc.json().get('status','?')})\n")
    except Exception:
        print(f"  {RED}Cannot reach backend at {base}{RESET}")
        print("  Start it with:  uvicorn app.main:app --reload --port 8000\n")
        sys.exit(1)

    print(f"  Firing {len(tickets)} ticket(s) with {args.delay}s delay...\n")
    print(f"  {'#':>3}  {'CATEGORY':<10} {'URGENCY':<10} {'STATUS':<10} {'CHECK':<5}  MESSAGE")
    print(f"  {'-'*70}")

    summary = {"pass": 0, "warn": 0, "fail": 0}

    for raw_idx, t in tickets:
        idx = raw_idx + 1
        payload = {
            "message": t["message"],
            "phone":   t["phone"],
            "lat":     t["lat"],
            "lng":     t["lng"],
        }

        data = fire_ticket(base, payload, idx, t)
        if data is None:
            summary["fail"] += 1
            continue

        cat     = data.get("category", "?")
        urg     = data.get("urgency",  "?")
        status  = data.get("status",   "?")
        check   = check_expectation(data, t)

        uc = URGENCY_COLOUR.get(urg, "")
        sc = STATUS_COLOUR.get(status, "")
        cc = GREEN if "[OK]" in check else ORANGE

        if "[OK]" in check:
            summary["pass"] += 1
        else:
            summary["warn"] += 1

        msg_preview = t["message"][:45].ljust(45)
        print(
            f"  [{idx:02d}]  "
            f"{uc}{cat:<10}{RESET} "
            f"{uc}{urg:<10}{RESET} "
            f"{sc}{status:<10}{RESET} "
            f"{cc}{check:<5}{RESET}  "
            f"{msg_preview}"
        )

        time.sleep(args.delay)

    # Summary
    total = len(tickets)
    print(f"\n  {'-'*70}")
    print(f"  {BOLD}Results: {GREEN}{summary['pass']} passed{RESET}  "
          f"{ORANGE}{summary['warn']} warnings{RESET}  "
          f"{RED}{summary['fail']} failed{RESET}  (of {total})")

    print(f"\n  {BOLD}Next steps:{RESET}")
    print(f"    Dashboard → http://localhost:5173")
    print(f"    Map View  → http://localhost:5173/map")
    print(f"    API Docs  → {base}/docs")
    print(f"    Tickets   → {base}/requests\n")


if __name__ == "__main__":
    main()
