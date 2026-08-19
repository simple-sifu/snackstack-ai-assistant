"""
Static data: order database.

In production these would come from a real database. For the demo
they are plain Python structures so you can see everything at a glance.
"""

from __future__ import annotations
from snackstack.config import get_logger

logger = get_logger("orders")

logger.info("ORDER_DATABASE loaded")

# ── Order Database ───────────────────────────────────────────
ORDER_DATABASE: dict[str, dict] = {
    "ORD-201": {
        "item": "Butter Chicken",
        "customer_name": "Priya Nair",
        "status": "Out for Delivery",
        "tracking": "SS201TRK",
        "customer_email": "priya@example.com",
    },
    "ORD-202": {
        "item": "Margherita Pizza",
        "customer_name": "Arjun Mehta",
        "status": "Placed",
        "tracking": "SS202TRK",
        "customer_email": "arjun@example.com",
    },
    "ORD-203": {
        "item": "Cheeseburger",
        "customer_name": "Sneha Roy",
        "status": "Preparing",
        "tracking": "SS203TRK",
        "customer_email": "sneha@example.com",
    },
    "ORD-204": {
        "item": "Buddha Bowl",
        "customer_name": "Rahul Das",
        "status": "Delivered",
        "tracking": "SS204TRK",
        "customer_email": "rahul@example.com",
    },
    "ORD-205": {
        "item": "Paneer Tikka",
        "customer_name": "Kavya Sharma",
        "status": "Placed",
        "tracking": "SS205TRK",
        "customer_email": "kavya@example.com",
    },
}
