import { URGENCY_LEVELS, URGENCY_STYLE, CATEGORY_ICON } from "../utils/urgency.js";

// Toggle chips for urgency + category. `filters` = { urgency: Set, category: Set }
export default function FilterBar({ filters, onToggle, counts }) {
  return (
    <div className="filter-bar">
      {URGENCY_LEVELS.map((u) => {
        const on = filters.urgency.has(u);
        return (
          <button
            key={u}
            className={`chip ${on ? "on" : ""}`}
            style={on ? { background: URGENCY_STYLE[u].color, borderColor: URGENCY_STYLE[u].color } : {}}
            onClick={() => onToggle("urgency", u)}
          >
            {URGENCY_STYLE[u].label} ({counts.urgency[u] || 0})
          </button>
        );
      })}
      <span className="divider" />
      {Object.keys(CATEGORY_ICON).map((c) => {
        const on = filters.category.has(c);
        return (
          <button key={c} className={`chip ${on ? "on dark" : ""}`} onClick={() => onToggle("category", c)}>
            {CATEGORY_ICON[c]} {c} ({counts.category[c] || 0})
          </button>
        );
      })}
    </div>
  );
}
