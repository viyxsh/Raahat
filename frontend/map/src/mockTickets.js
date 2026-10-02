// Sample tickets around Bhopal so the map works before the backend is ready.
// Same shape as the real GET /requests response.
// created_at mimics the backend: UTC, no "Z" (SQLite drops the timezone).
const minutesAgo = (m) => new Date(Date.now() - m * 60000).toISOString().replace("Z", "");

export const MOCK_TICKETS = [
  { id: 1, text: "NEED WATER SECTOR 3", phone: "+911234567890", lat: 23.21, lng: 77.41, category: "water", urgency: "high", status: "new", created_at: minutesAgo(4) },
  { id: 2, text: "old man injured bleeding near bus stand", phone: "+919800000001", lat: 23.2599, lng: 77.4126, category: "medical", urgency: "critical", status: "verified", created_at: minutesAgo(12) },
  { id: 3, text: "house roof collapsed 6 people need shelter", phone: "+919800000002", lat: 23.2335, lng: 77.4343, category: "shelter", urgency: "high", status: "assigned", created_at: minutesAgo(25) },
  { id: 4, text: "need water sector 3 pls", phone: "+919800000003", lat: 23.2112, lng: 77.4109, category: "water", urgency: "medium", status: "flagged", created_at: minutesAgo(3) },
  { id: 5, text: "pregnant woman labour pain no ambulance", phone: "+919800000004", lat: 23.1815, lng: 77.4580, category: "medical", urgency: "critical", status: "new", created_at: minutesAgo(1) },
  { id: 6, text: "food packets required for 20 families", phone: "+919800000005", lat: 23.2700, lng: 77.3900, category: "other", urgency: "medium", status: "new", created_at: minutesAgo(40) },
  { id: 7, text: "drinking water tanker not reached ward 12", phone: "+919800000006", lat: 23.2450, lng: 77.4700, category: "water", urgency: "low", status: "verified", created_at: minutesAgo(90) },
  { id: 8, text: "blankets needed at relief camp", phone: "+919800000007", lat: 23.1950, lng: 77.3800, category: "shelter", urgency: "low", status: "new", created_at: minutesAgo(65) },
  // Just arrived, classifier (Task 4) hasn't run yet -> category/urgency are null
  { id: 9, text: "help needed near railway station", phone: "+919800000008", lat: 23.2668, lng: 77.4116, category: null, urgency: null, status: "new", created_at: minutesAgo(0) },
];
