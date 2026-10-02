// Polls the backend every REFRESH_MS and keeps the latest ticket list.
// Shared hook — Task 1's dashboard can use the same one.
import { useCallback, useEffect, useRef, useState } from "react";
import { fetchTickets } from "../api.js";

const REFRESH_MS = Number(import.meta.env.VITE_REFRESH_MS) || 5000;

export function useTickets() {
  const [tickets, setTickets] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [newIds, setNewIds] = useState(new Set()); // tickets that arrived since the last refresh
  const knownIds = useRef(null);

  const refresh = useCallback(async () => {
    try {
      const data = await fetchTickets();
      // Work out which tickets are new so the map can pulse them
      if (knownIds.current) {
        const fresh = new Set(data.filter((t) => !knownIds.current.has(t.id)).map((t) => t.id));
        setNewIds(fresh);
      }
      knownIds.current = new Set(data.map((t) => t.id));
      setTickets(data);
      setError(null);
      setLastUpdated(new Date());
    } catch (e) {
      // Keep showing the last good data; just report the error
      setError(e.message || "Could not reach backend");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    const timer = setInterval(refresh, REFRESH_MS);
    return () => clearInterval(timer);
  }, [refresh]);

  return { tickets, error, loading, lastUpdated, newIds, refresh, refreshMs: REFRESH_MS };
}
