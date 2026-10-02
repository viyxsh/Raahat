import { URGENCY_LEVELS, URGENCY_STYLE, CATEGORY_ICON, UNCLASSIFIED } from "../utils/urgency.js";

export default function Legend() {
  return (
    <div className="legend">
      <div className="legend-title">Urgency</div>
      {URGENCY_LEVELS.map((u) => (
        <div key={u} className="legend-row">
          <span
            className="legend-dot"
            style={{
              background: URGENCY_STYLE[u].color,
              width: URGENCY_STYLE[u].radius * 1.6,
              height: URGENCY_STYLE[u].radius * 1.6,
            }}
          />
          {URGENCY_STYLE[u].label}
        </div>
      ))}
      <div className="legend-row">
        <span className="legend-dot" style={{ background: UNCLASSIFIED.color, width: 13, height: 13 }} />
        Not classified yet
      </div>
      <div className="legend-title" style={{ marginTop: 8 }}>Category</div>
      {Object.entries(CATEGORY_ICON).map(([c, icon]) => (
        <div key={c} className="legend-row">
          <span style={{ width: 18, textAlign: "center" }}>{icon}</span>
          {c[0].toUpperCase() + c.slice(1)}
        </div>
      ))}
      <div className="legend-note">Dashed ring = flagged duplicate</div>
    </div>
  );
}
