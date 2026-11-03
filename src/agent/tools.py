"""Agent tools: deterministic query functions exposed to the LLM.

Each tool returns JSON-serializable data. ``TOOL_SPECS`` holds the JSON schemas
used for OpenAI-style function calling; ``StoreTools.dispatch`` routes a tool call
by name.
"""

from __future__ import annotations

from typing import Any

from ..data.policies import PolicyIndex
from ..data.store import DataStore
from ..data.text import normalize

STORE_INFO: dict[str, Any] = {
    "name": "Empório da Música",
    "founded": 2008,
    "address": "Rua 14 de Maio, 3200 — Centro, Campo Grande-MS, 79202-333",
    "phone_whatsapp": "(67) 3341-4444",
    "whatsapp_service": "(67) 3321-4500",
    "email": "contato@emporiodamusica.com.br",
    "hours": {
        "monday_to_friday": "09:00-18:00",
        "saturday": "09:00-13:00",
        "sunday_holidays": "closed",
    },
    "scope": (
        "Sells exclusively musical instruments (guitars, basses, acoustic guitars, "
        "drums, keyboards, winds, orchestral strings, ukuleles). Does not sell accessories."
    ),
}

TOOL_SPECS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Search the store catalog by text, category and/or price range. "
                "Use for questions like 'acoustic guitars under R$1000'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Free-text search (name/brand/type)."},
                    "category": {"type": "string", "description": "Category filter, e.g. 'Violões'."},
                    "max_price": {"type": "number", "description": "Maximum price in BRL."},
                    "min_price": {"type": "number", "description": "Minimum price in BRL."},
                    "only_available": {
                        "type": "boolean",
                        "description": "Only in-stock active products (default true).",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": "Get a single product's price, stock, status and promotion by name or id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Product name or model, e.g. 'Takamine GD20'."},
                    "product_id": {"type": "integer", "description": "Product id."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get an order's status, dates and tracking by order id or tracking code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "Order id."},
                    "tracking_code": {"type": "string", "description": "Tracking code, e.g. BRAB1234567BR."},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_policies",
            "description": "Answer questions about store policies (returns, hours, payment, shipping, warranty).",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The customer's policy question."},
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calc_shipping",
            "description": "Estimate shipping cost/options for a city and order total.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Destination city."},
                    "order_total": {"type": "number", "description": "Order total in BRL."},
                },
                "required": ["city", "order_total"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_store_info",
            "description": "Get store contact details, address and business hours.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


class StoreTools:
    """Implementation of the agent tools backed by the data store and policies."""

    def __init__(self, store: DataStore, policies: PolicyIndex) -> None:
        self.store = store
        self.policies = policies

    # ------------------------------------------------------------------ tools
    def search_products(
        self,
        query: str | None = None,
        category: str | None = None,
        max_price: float | None = None,
        min_price: float | None = None,
        only_available: bool = True,
        limit: int = 10,
    ) -> dict[str, Any]:
        products = self.store.search_products(
            query=query,
            category=category,
            max_price=max_price,
            min_price=min_price,
            only_available=only_available,
            limit=limit,
        )
        return {"count": len(products), "products": products}

    def get_product(
        self, name: str | None = None, product_id: int | None = None
    ) -> dict[str, Any]:
        product = self.store.get_product(name=name, product_id=product_id)
        return {"found": product is not None, "product": product}

    def get_order_status(
        self, order_id: int | None = None, tracking_code: str | None = None
    ) -> dict[str, Any]:
        order = self.store.get_order(order_id=order_id, tracking_code=tracking_code)
        return {"found": order is not None, "order": order}

    def query_policies(self, question: str) -> dict[str, Any]:
        results = self.policies.search(question, top_k=2)
        return {"found": bool(results), "results": results}

    def calc_shipping(self, city: str, order_total: float) -> dict[str, Any]:
        is_metro = "campo grande" in normalize(city)
        if is_metro:
            free = float(order_total) >= 500.0
            return {
                "city": city,
                "region": "Campo Grande (metropolitan)",
                "free_shipping": free,
                "cost": 0.0 if free else 35.0,
                "eta": "1-3 business days",
                "note": "Delivered by our own courier; the customer is contacted before delivery.",
            }
        return {
            "city": city,
            "region": "other city",
            "free_shipping": False,
            "cost": None,
            "options": [
                {"carrier": "Correios PAC", "eta": "5-12 business days"},
                {"carrier": "Correios SEDEX", "eta": "2-5 business days"},
                {"carrier": "Jadlog", "eta": "3-8 business days"},
            ],
            "note": (
                "Shipping is quoted by destination ZIP, weight and dimensions. "
                "Large instruments may need an individual quote."
            ),
        }

    def get_store_info(self) -> dict[str, Any]:
        return dict(STORE_INFO)

    # --------------------------------------------------------------- dispatch
    def dispatch(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        args = arguments or {}
        handlers = {
            "search_products": self.search_products,
            "get_product": self.get_product,
            "get_order_status": self.get_order_status,
            "query_policies": self.query_policies,
            "calc_shipping": self.calc_shipping,
            "get_store_info": self.get_store_info,
        }
        handler = handlers.get(name)
        if handler is None:
            return {"error": f"Unknown tool: {name}"}
        try:
            return handler(**args)
        except TypeError as exc:  # bad arguments from the model
            return {"error": f"Invalid arguments for {name}: {exc}"}
