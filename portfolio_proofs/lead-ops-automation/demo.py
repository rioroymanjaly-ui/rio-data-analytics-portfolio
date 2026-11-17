"""Standalone synthetic operations triage demo; NOT source code from RUIYA."""

import json
import re
from pathlib import Path

PRODUCTS = {"steel": "steel", "aluminium": "aluminium",
            "aluminum": "aluminium", "copper": "copper"}
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
QUANTITY = re.compile(r"\b(\d{1,6})\s*(?:kg|kilograms)\b", re.I)


def triage_request(request):
    """Return a structured decision; all commercial actions require a human."""
    message = request.get("message", "")
    if not isinstance(message, str):
        raise ValueError("message must be text")
    request_id = request.get("request_id")
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("request_id required")

    matches = sorted(set(name for keyword, name in PRODUCTS.items()
                         if re.search(r"\b" + keyword + r"\b", message.lower())))
    quantity = QUANTITY.search(message)
    email = EMAIL.search(message)
    missing = []
    if len(matches) != 1:
        missing.append("one clear material")
    if not quantity:
        missing.append("quantity in kg")
    if not email:
        missing.append("email contact")

    return {
        "request_id": request_id,
        "material": matches[0] if len(matches) == 1 else None,
        "quantity_kg": int(quantity.group(1)) if quantity else None,
        "email": email.group(0) if email else None,
        "status": "needs_clarification" if missing else "ready_for_human_review",
        "missing": missing,
        "next_action": "request_missing_details" if missing else "human_validate_and_prepare_quote",
        "human_approval_required": True,
        "evidence": {
            "material_matches": matches,
            "quantity_match": quantity.group(0) if quantity else None,
            "contact_match": email.group(0) if email else None,
        }
    }


def process_requests(requests):
    seen = set()
    output = []
    for request in requests:
        request_id = request.get("request_id")
        if request_id in seen:
            raise ValueError(f"duplicate request_id: {request_id}")
        seen.add(request_id)
        output.append(triage_request(request))
    return output


if __name__ == "__main__":
    data = json.loads((Path(__file__).parent / "synthetic_requests.json").read_text())
    output = process_requests(data)
    print(json.dumps(output, indent=2))
    print("Summary:", {name: sum(item["status"] == name for item in output)
          for name in ("ready_for_human_review", "needs_clarification")})
