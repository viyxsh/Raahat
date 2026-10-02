// Task 2 — Live Map View
// Plots every ticket as a circle marker coloured by urgency.
// Reusable: <MapView tickets={...} /> — Task 1 can embed it in the dashboard.
import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, Tooltip, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import {
  urgencyStyle,
  hasValidCoords,
  sortForDrawing,
  categoryLabel,
  STATUS_LABEL,
  timeAgo,
} from "../utils/urgency.js";

const DEFAULT_CENTER = [23.2599, 77.4126]; // Bhopal
const DEFAULT_ZOOM = 12;

// Zoom to fit all markers the first time data arrives (not on every refresh,
// otherwise the map would jump while the coordinator is panning).
function FitToTickets({ tickets, fitKey }) {
  const map = useMap();
  useEffect(() => {
    if (!tickets.length) return;
    if (tickets.length === 1) {
      map.setView([tickets[0].lat, tickets[0].lng], 14);
      return;
    }
    const bounds = tickets.map((t) => [t.lat, t.lng]);
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fitKey, map]);
  return null;
}

// Pans to a ticket when it is selected from outside (e.g. dashboard list click)
function FlyToSelected({ ticket }) {
  const map = useMap();
  useEffect(() => {
    if (ticket && hasValidCoords(ticket)) {
      map.flyTo([ticket.lat, ticket.lng], Math.max(map.getZoom(), 15), { duration: 0.6 });
    }
  }, [ticket, map]);
  return null;
}

export default function MapView({ tickets, newIds = new Set(), selected = null, onSelect, fitKey = 0 }) {
  const plottable = sortForDrawing(tickets.filter(hasValidCoords));

  return (
    <MapContainer center={DEFAULT_CENTER} zoom={DEFAULT_ZOOM} className="map" scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <FitToTickets tickets={plottable} fitKey={fitKey} />
      <FlyToSelected ticket={selected} />

      {plottable.map((t) => {
        const s = urgencyStyle(t.urgency);
        const isNew = newIds.has(t.id);
        const isFlagged = t.status === "flagged";
        const isSelected = selected && selected.id === t.id;
        return (
          <CircleMarker
            key={t.id}
            center={[t.lat, t.lng]}
            radius={isSelected ? s.radius + 4 : s.radius}
            pathOptions={{
              color: isFlagged ? "#212121" : "#ffffff",
              weight: isFlagged || isSelected ? 3 : 2,
              dashArray: isFlagged ? "4 3" : null,
              fillColor: s.color,
              fillOpacity: t.status === "assigned" ? 0.45 : 0.9,
              className: isNew ? "marker-new" : "",
            }}
            eventHandlers={{ click: () => onSelect && onSelect(t) }}
          >
            <Tooltip direction="top" offset={[0, -s.radius]}>
              {categoryLabel(t.category)} · {s.label}
            </Tooltip>
            <Popup>
              <div className="popup">
                <div className="popup-head">
                  <span className="badge" style={{ background: s.color }}>{s.label}</span>
                  <span className="popup-cat">{categoryLabel(t.category)}</span>
                </div>
                <div className="popup-text">“{t.text}”</div>
                <table className="popup-meta">
                  <tbody>
                    <tr><td>Ticket</td><td>#{t.id}</td></tr>
                    <tr><td>Status</td><td>{STATUS_LABEL[t.status] || t.status}</td></tr>
                    <tr><td>Phone</td><td>{t.phone}</td></tr>
                    <tr><td>Received</td><td>{timeAgo(t.created_at)}</td></tr>
                    <tr><td>Location</td><td>{t.lat.toFixed(4)}, {t.lng.toFixed(4)}</td></tr>
                  </tbody>
                </table>
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}
