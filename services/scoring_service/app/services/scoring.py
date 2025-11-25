from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Iterable

from app.models.normalized_event import NormalizedEvent


def compute_score(events: Iterable[NormalizedEvent]) -> tuple[int, str, dict]:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=365)

    filtered = [e for e in events if (e.event_date or e.created_at) >= cutoff]

    base_score = 100
    score = base_score

    severity_counts = Counter()
    type_counts = Counter()

    for e in filtered:
        severity_counts[e.severity] += 1
        type_counts[e.event_type] += 1

        if e.severity == "high":
            score -= 20
        elif e.severity == "medium":
            score -= 10
        elif e.severity == "low":
            score -= 3

    score = max(0, min(100, score))

    if score <= 40:
        risk_level = "high"
    elif score <= 70:
        risk_level = "medium"
    else:
        risk_level = "low"

    details = {
        "base_score": base_score,
        "final_score": score,
        "severity_counts": dict(severity_counts),
        "type_counts": dict(type_counts),
        "events_considered": len(filtered),
    }

    return score, risk_level, details
