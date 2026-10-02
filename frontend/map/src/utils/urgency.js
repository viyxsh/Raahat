// Single source of truth for urgency/category/status styling.
// Task 1 (dashboard badges) can import from here too so both screens match.

export const URGENCY_LEVELS = ["critical", "high", "medium", "low"];

export const URGENCY_STYLE = {
  critical: { color: "#C62828", label: "Critical", radius: 13, rank: 4 },
  high: { color: "#EF6C00", label: "High", radius: 11, rank: 3 },
  medium: { color: "#F9A825", label: "Medium", radius: 9, rank: 2 },
  low: { color: "#2E7D32", label: "Low", radius: 7, rank: 1 },
};

export const CATEGORY_ICON = {
  medical: "🩺",
  water: "💧",
  shelter: "🏠",
  other: "❓",
};

// Backend stores category/urgency as null until the classifier (Task 4) runs.
export const UNCLASSIFIED = { color: "#78909C", label: "Unclassified", radius: 8, rank: 0 };

export function categoryLabel(category) {
  return category ? `${CATEGORY_ICON[category] || "❓"} ${category}` : "⏳ Not classified yet";
}

export const STATUS_LABEL = {
  new: "New",
  flagged: "Flagged (possible duplicate)",
  verified: "Verified",
  assigned: "Assigned",
};

// Fallback so an unexpected value from the classifier never crashes the map.
export function urgencyStyle(urgency) {
  if (!urgency) return UNCLASSIFIED;
  return URGENCY_STYLE[urgency] || { ...UNCLASSIFIED, label: urgency };
}

// The backend uses SQLite, which drops the timezone, so created_at arrives as
// "2026-10-03T19:05:12.123456" with no "Z". It is UTC; without this fix the
// browser would read it as Indian time and every ticket would be 5.5 h off.
export function parseServerTime(iso) {
  if (!iso) return null;
  const hasZone = /([zZ]|[+-]\d{2}:?\d{2})$/.test(iso);
  return new Date(hasZone ? iso : iso + "Z");
}

// A ticket can only be drawn if it has real coordinates.
export function hasValidCoords(t) {
  return (
    typeof t.lat === "number" &&
    typeof t.lng === "number" &&
    !Number.isNaN(t.lat) &&
    !Number.isNaN(t.lng) &&
    t.lat >= -90 && t.lat <= 90 &&
    t.lng >= -180 && t.lng <= 180
  );
}

// Draw low first, critical last, so critical markers sit on top.
export function sortForDrawing(tickets) {
  return [...tickets].sort((a, b) => urgencyStyle(a.urgency).rank - urgencyStyle(b.urgency).rank);
}

export function timeAgo(iso) {
  const d = parseServerTime(iso);
  const then = d ? d.getTime() : NaN;
  if (Number.isNaN(then)) return "";
  const s = Math.max(0, Math.round((Date.now() - then) / 1000));
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.round(s / 60)} min ago`;
  if (s < 86400) return `${Math.round(s / 3600)} h ago`;
  return d.toLocaleString();
}
