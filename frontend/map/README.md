# Raahat — Frontend (Task 2: Live Map View)

React + Leaflet map that plots every help-request ticket by location, coloured by urgency, and auto-refreshes from the backend.

## Run it

```bash
cd frontend/map
npm install
cp .env.example .env        # VITE_USE_MOCK=true -> works without backend
npm run dev                 # open http://localhost:5173
```

### Switch to the real backend (when Vinit's Task 3 is up)
1. Start the backend on port 8000 (`uvicorn app.main:app --reload --port 8000`).
2. In `.env` set `VITE_USE_MOCK=false`.
3. Restart `npm run dev`.

The Vite dev server forwards `/api/*` → `http://localhost:8000/*`, so no CORS setup is needed during development.

### Create a test ticket and watch it appear
```bash
curl -X POST http://localhost:8000/simulate/sms \
  -H "Content-Type: application/json" \
  -d '{"message":"NEED WATER SECTOR 3","phone":"+911234567890","lat":23.21,"lng":77.41}'
```
Within one refresh interval (default 5 s) the marker appears on the map and pulses.

## Files

| File | What it does |
|---|---|
| `src/components/MapView.jsx` | The Leaflet map: markers, popups, tooltips, auto-fit, fly-to-selected. **Reusable** — Task 1 can embed `<MapView tickets={...} />` |
| `src/components/MapPage.jsx` | Full map screen: header, filters, legend, status bar |
| `src/components/FilterBar.jsx` | Urgency/category toggle chips with counts |
| `src/components/Legend.jsx` | Colour/category legend on the map |
| `src/hooks/useTickets.js` | Polls `GET /requests` every N seconds, tracks newly arrived tickets. **Shared** with Task 1 |
| `src/api.js` | `fetchTickets()` and `simulateSms()` |
| `src/utils/urgency.js` | Colours, sizes, labels for urgency/category/status. Task 1 badges should use this too |
| `src/mockTickets.js` | Sample tickets around Bhopal for offline development |

## Map rules

| Ticket property | How it shows on the map |
|---|---|
| urgency | Marker colour + size: critical (red, largest) → high (orange) → medium (yellow) → low (green, smallest). Critical is drawn on top |
| category | Icon in tooltip/popup: 🩺 medical, 💧 water, 🏠 shelter, ❓ other |
| status = flagged | Dashed dark ring (possible duplicate from Task 4) |
| status = assigned | Faded marker (already being handled) |
| new since last refresh | Pulses a few times |
| missing/invalid lat-lng | Not plotted; counted in the status bar ("N without location") |

## Config (`.env`)

| Variable | Default | Meaning |
|---|---|---|
| `VITE_USE_MOCK` | `true` | Use sample data instead of the backend |
| `VITE_REFRESH_MS` | `5000` | Auto-refresh interval |
| `VITE_BACKEND_URL` | `http://localhost:8000` | Where `/api` is proxied |
