from typing import Any, Dict, List


def classify_events(raw_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []

    for raw in raw_events:
        company_id = raw.get("company_id")
        source = raw.get("source", "unknown")
        payload = raw.get("payload", {})

        text = ""
        if isinstance(payload, dict):
            text = str(payload)

        text_lower = text.lower()

        if any(word in text_lower for word in ["банкротство", "liquidation", "банкрот"]):
            event_type = "bankruptcy_risk"
            severity = "high"
            description = "Potential bankruptcy-related signal detected"
        elif any(word in text_lower for word in ["штраф", "penalty", "fine"]):
            event_type = "regulatory_penalty"
            severity = "medium"
            description = "Possible regulatory penalty signal"
        else:
            event_type = "general_activity"
            severity = "low"
            description = "General company activity signal"

        normalized.append(
            {
                "company_id": company_id,
                "event_type": event_type,
                "severity": severity,
                "description": description,
                "source": source,
                "event_date": None,
                "meta": {
                    "raw_id": payload.get("id") if isinstance(payload, dict) else None,
                    "raw_source": source,
                },
            }
        )

    return normalized
