"""Revenue event tracking utilities."""

from datetime import datetime, timezone


def track_revenue_event(event_type: str, payload: dict) -> None:
    """Track a revenue-related event (placeholder for DB/analytics integration)."""
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] event={event_type} payload={payload}")
