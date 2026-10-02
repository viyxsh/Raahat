// Full-screen Live Map page: header + filters + map + legend + status bar.
import { useMemo, useState } from "react";
import MapView from "./MapView.jsx";
import Legend from "./Legend.jsx";
import FilterBar from "./FilterBar.jsx";
import { useTickets } from "../hooks/useTickets.js";
import { hasValidCoords, URGENCY_LEVELS, CATEGORY_ICON } from "../utils/urgency.js";
import { isMockMode } from "../api.js";

const ALL_URGENCY = new Set(URGENCY_LEVELS);
const ALL_CATEGORY = new Set(Object.keys(CATEGORY_ICON));

export default function MapPage() {
  const { tickets, error, loading, lastUpdated, newIds, refresh, refreshMs } = useTickets();
  const [filters, setFilters] = useState({ urgency: new Set(ALL_URGENCY), category: new Set(ALL_CATEGORY) });
  const [selected, setSelected] = useState(null);
  const [fitKey, setFitKey] = useState(0);
  const [hasFitted, setHasFitted] = useState(false);

  // Fit the map once, when the first batch of tickets arrives
  if (!hasFitted && tickets.length > 0) {
    setHasFitted(true);
    setFitKey((k) => k + 1);
  }

  const toggle = (kind, value) =>
    setFilters((f) => {
      const next = new Set(f[kind]);
      next.has(value) ? next.delete(value) : next.add(value);
      return { ...f, [kind]: next };
    });

  const counts = useMemo(() => {
    const c = { urgency: {}, category: {} };
    tickets.forEach((t) => {
      c.urgency[t.urgency] = (c.urgency[t.urgency] || 0) + 1;
      c.category[t.category] = (c.category[t.category] || 0) + 1;
    });
    return c;
  }, [tickets]);

  const visible = tickets.filter(
    (t) =>
      (filters.urgency.has(t.urgency) || !ALL_URGENCY.has(t.urgency)) &&
      (filters.category.has(t.category) || !ALL_CATEGORY.has(t.category))
  );
  const noLocation = tickets.filter((t) => !hasValidCoords(t)).length;
  const critical = tickets.filter((t) => t.urgency === "critical" && t.status !== "assigned").length;

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>Raahat — Live Map</h1>
          <span className="sub">Help requests plotted by location and urgency</span>
        </div>
        <div className="header-right">
          {critical > 0 && <span className="alert">⚠ {critical} critical unassigned</span>}
          {isMockMode && <span className="mock">MOCK DATA</span>}
          <button className="refresh" onClick={refresh}>↻ Refresh</button>
          <button className="refresh" onClick={() => setFitKey((k) => k + 1)}>⤢ Fit all</button>
        </div>
      </header>

      <FilterBar filters={filters} onToggle={toggle} counts={counts} />

      <div className="map-wrap">
        <MapView tickets={visible} newIds={newIds} selected={selected} onSelect={setSelected} fitKey={fitKey} />
        <Legend />
        {loading && <div className="overlay">Loading tickets…</div>}
      </div>

      <footer className="status-bar">
        <span>
          Showing {visible.filter(hasValidCoords).length} of {tickets.length} tickets
          {noLocation > 0 && ` · ${noLocation} without location`}
        </span>
        <span className={error ? "err" : ""}>
          {error
            ? `Backend error: ${error} (showing last data)`
            : lastUpdated
            ? `Updated ${lastUpdated.toLocaleTimeString()} · auto-refresh every ${refreshMs / 1000}s`
            : ""}
        </span>
      </footer>
    </div>
  );
}
