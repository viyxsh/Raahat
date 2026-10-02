// Talks to Vinit's backend (Task 3).
// Contract: GET /requests -> { "tickets": [ {id, text, phone, lat, lng, category, urgency, status, created_at}, ... ] }
import { MOCK_TICKETS } from "./mockTickets.js";

const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true";

export async function fetchTickets() {
  if (USE_MOCK) {
    return MOCK_TICKETS;
  }
  const res = await fetch("/api/requests");
  if (!res.ok) throw new Error(`Backend returned ${res.status}`);
  const data = await res.json();
  if (!data || !Array.isArray(data.tickets)) {
    throw new Error("Unexpected response: expected { tickets: [...] }");
  }
  return data.tickets;
}

// Handy for the demo: create a ticket from the map screen via POST /simulate/sms
export async function simulateSms({ message, phone, lat, lng }) {
  const res = await fetch("/api/simulate/sms", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, phone, lat, lng }),
  });
  if (!res.ok) throw new Error(`Backend returned ${res.status}`);
  return res.json();
}

export const isMockMode = USE_MOCK;
