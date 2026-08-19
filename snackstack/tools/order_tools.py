"""
Order Tools — the concrete actions agents can take.

Sales Support (1 tools):
  • get_order_status        – order lookup by ID or email
"""

from __future__ import annotations

from langchain_core.tools import tool

from snackstack.logger import get_logger
from snackstack.data.orders import ORDER_DATABASE

logger = get_logger("order_tools")


# ── helpers ──────────────────────────────────────────────────

def normalise_order_id(raw: str) -> str:
    """Accept 'ORD-201', 'ORD201', 'ord-201', or just '201' → 'ORD-201'."""
    upper = raw.upper().strip()
    clean = upper.replace("ORD-", "").replace("ORD", "").strip()
    return f"ORD-{clean}"

def normalise_tracking_order(raw: str) -> str:
    """Accept 'SS203TRK', 'ss203trk' → 'SS203TRK'."""
    upper = raw.upper().strip()
    clean = upper.replace("SS", "").replace("TRK", "").strip()
    return f"SS{clean}TRK"

def lookup_order_by_email(email: str) -> dict | None:
    """Find the first order matching a customer email."""
    email_lower = email.lower().strip()
    for oid, order in ORDER_DATABASE.items():
        if order["customer_email"].lower() == email_lower:
            return {"order_id": oid, **order}
    return None


def lookup_order_by_tracking(tracking: str) -> dict | None:
    """Find the first order matching a tracking ID."""
    tracking_id = normalise_tracking_order(tracking)
    for oid, order in ORDER_DATABASE.items():
        if order["tracking"].upper() == tracking_id:
            return {"order_id": oid, **order}
    return None

# ═══════════════════════════════════════════════════════════
#  SALES SUPPORT TOOLS
# ═══════════════════════════════════════════════════════════

@tool
def get_order_status(identifier: str) -> str:
    """Look up the current status of a customer order.

    Args:
        identifier: an order ID (e.g. "ORD101") OR tracking ID, 
        or a customer email address
    """
    logger.info("get_order_status  identifier=%r", identifier)

    if "@" in identifier:
        match = lookup_order_by_email(identifier)
        if not match:
            return f"No order found for email: {identifier}"
        oid = match["order_id"]
        order = {k: v for k, v in match.items() if k != "order_id"}
    elif "ORD-" in identifier.upper():
        oid = normalise_order_id(identifier)
        order = ORDER_DATABASE.get(oid)
        if not order:
            return f"Order {oid} not found. Please verify the order ID."
    elif "TRK" in identifier.upper():
        match = lookup_order_by_tracking(identifier)
        if not match:
            return f"No order found for tracking ID: {identifier}"
        oid = match["order_id"]
        order = {k: v for k, v in match.items() if k != "order_id"}
    else:
        return (
            f"Could not recognise '{identifier}'. "
            "Provide an order ID (ORD-201), tracking ID (SS201TRK), or email."
        )

    info = (
        f"Order {oid}:\n"
        f"  Customer : {order['customer_name']} ({order['customer_email']})\n"
        f"  Item     : {order['item']}\n"
        f"  Status   : {order['status']}\n"
        f"  Tracking : {order['tracking']}"
    )
    return info

