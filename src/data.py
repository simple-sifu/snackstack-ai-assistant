"""
Static data: Menu catalog, order database, and support policies.

In production these would come from a real database. For the demo
they are plain Python structures so you can see everything at a glance.
"""

from __future__ import annotations
from src.config import get_logger

logger = get_logger("data")

logger.info("MENU_CATALOG & ORDER_DATABASE loaded")

# ── Menu Catalog (used by RAG) ──────────────────────────────
MENU_CATALOG: list[dict] = [
    {
        "id": "DISH001",
        "name": "Margherita Pizza",
        "category": "Pizza",
        "cuisine": "Italian",
        "price": 299,
        "rating": 4.7,
        "dietary_tags": ["vegetarian"],
        "description": "Classic thin crust with tomato, mozzarella, basil",
        "availability": True,
    },
    {
        "id": "DISH002",
        "name": "Vegan Pasta Primavera",
        "category": "Pasta",
        "cuisine": "Italian",
        "price": 349,
        "rating": 4.5,
        "dietary_tags": ["vegan"],
        "description": "Penne with seasonal vegetables, olive oil, garlic",
        "availability": True,
    },
    {
        "id": "DISH003",
        "name": "Butter Chicken",
        "category": "Mains",
        "cuisine": "Indian",
        "price": 379,
        "rating": 4.9,
        "dietary_tags": ["gluten-free"],
        "description": "Creamy tomato curry with tender chicken and naan",
        "availability": True,
    },
    {
        "id": "DISH004",
        "name": "Vegan Buddha Bowl",
        "category": "Bowls",
        "cuisine": "Fusion",
        "price": 319,
        "rating": 4.6,
        "dietary_tags": ["vegan", "gluten-free"],
        "description": "Quinoa, chickpeas, avocado, greens, tahini",
        "availability": True,
    },
    {
        "id": "DISH005",
        "name": "Classic Cheeseburger",
        "category": "Burgers",
        "cuisine": "American",
        "price": 259,
        "rating": 4.4,
        "dietary_tags": [],
        "description": "Beef patty, cheddar, lettuce, tomato, brioche bun",
        "availability": True,
    },
    {
        "id": "DISH006",
        "name": "Paneer Tikka",
        "category": "Starters",
        "cuisine": "Indian",
        "price": 199,
        "rating": 4.8,
        "dietary_tags": ["vegetarian", "gluten-free"],
        "description": "Tandoor-grilled cottage cheese with peppers",
        "availability": True,
    },
    {
        "id": "DISH007",
        "name": "Aglio e Olio",
        "category": "Pasta",
        "cuisine": "Italian",
        "price": 279,
        "rating": 4.5,
        "dietary_tags": ["vegan"],
        "description": "Spaghetti with garlic, chilli, olive oil, parsley",
        "availability": True,
    },
    {
        "id": "DISH008",
        "name": "Mango Lassi",
        "category": "Beverages",
        "cuisine": "Indian",
        "price": 99,
        "rating": 4.7,
        "dietary_tags": ["vegetarian", "gluten-free"],
        "description": "Blended yogurt with Alphonso mango, cardamom",
        "availability": True,
    },
]


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

# Mutable queue — filled at runtime by escalate_to_human tool
ESCALATION_QUEUE: list[dict] = []


# ── Support Policies (injected into Support Agent prompt) ──────
SUPPORT_POLICIES = """
SHIPPING OPTIONS:
- Rocket (Same-day): ₹199, available before 1 PM in metro cities
- Glide (3-4 days): ₹99, express delivery
- Cruise (7-8 days): Free on orders over ₹500

ESCALATION CRITERIA:
- Customer explicitly requests a human agent
- Complaint involves safety or legal issues
- Customer is highly frustrated or angry
- Issue cannot be resolved with available tools
""".strip()