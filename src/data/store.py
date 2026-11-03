"""In-memory SQLite data store built from the provided CSV files.

The dataset is small (dozens of rows), so the store loads everything into an
in-memory SQLite database on construction. Query helpers return plain ``dict``
objects so they are JSON-serializable and easy to feed to the LLM as tool output.

Normalized columns (``*_norm``) are added to enable accent/case-insensitive
matching without depending on SQLite's limited Unicode LIKE behaviour.
"""

from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any

from ..config import resolve_data_dir
from .text import normalize

CSV_PREFIX = "desafio_tecnico_ai_eng - "


class DataStore:
    """Loads the Empório da Música CSVs into an in-memory SQLite database."""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        self.data_dir = resolve_data_dir(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self._create_schema()
        self._load()

    # ------------------------------------------------------------------ loading
    def _csv_path(self, name: str) -> Path:
        return self.data_dir / f"{CSV_PREFIX}{name}.csv"

    def _read_rows(self, name: str) -> list[dict[str, str]]:
        with open(self._csv_path(name), newline="", encoding="utf-8-sig") as fh:
            return list(csv.DictReader(fh))

    def _create_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE categories (
                category_id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                name_norm TEXT
            );
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                price_brl REAL,
                name TEXT,
                category_id INTEGER,
                description TEXT,
                stock_quantity INTEGER,
                status TEXT,
                specs TEXT,
                created_at TEXT,
                name_norm TEXT,
                description_norm TEXT
            );
            CREATE TABLE customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT,
                city TEXT
            );
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date TEXT,
                status TEXT,
                total_brl REAL,
                payment_method TEXT,
                tracking_code TEXT,
                estimated_delivery TEXT,
                notes TEXT
            );
            CREATE TABLE order_items (
                order_id INTEGER,
                quantity INTEGER,
                product_id INTEGER
            );
            CREATE TABLE promotions (
                promotion_id INTEGER PRIMARY KEY,
                product_id INTEGER,
                discount_percent INTEGER,
                description TEXT,
                is_active INTEGER
            );
            """
        )

    def _load(self) -> None:
        cats = self._read_rows("categories")
        self.conn.executemany(
            "INSERT INTO categories VALUES (?, ?, ?, ?)",
            [
                (
                    int(c["category_id"]),
                    c["name"],
                    c.get("description", ""),
                    normalize(c["name"]),
                )
                for c in cats
            ],
        )

        products = self._read_rows("products")
        self.conn.executemany(
            "INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    int(p["product_id"]),
                    float(p["price_brl"]),
                    p["name"],
                    int(p["category_id"]),
                    p.get("description", ""),
                    int(float(p["stock_quantity"])),
                    p["status"],
                    p.get("specs", ""),
                    p.get("created_at", ""),
                    normalize(p["name"]),
                    normalize(p.get("description", "")),
                )
                for p in products
            ],
        )

        customers = self._read_rows("customers")
        self.conn.executemany(
            "INSERT INTO customers VALUES (?, ?, ?, ?, ?)",
            [
                (
                    int(c["customer_id"]),
                    c["name"],
                    c.get("phone", ""),
                    c.get("email", ""),
                    c.get("city", ""),
                )
                for c in customers
            ],
        )

        orders = self._read_rows("orders")
        self.conn.executemany(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    int(o["order_id"]),
                    int(o["customer_id"]),
                    o.get("order_date", ""),
                    o.get("status", ""),
                    float(o["total_brl"]) if o.get("total_brl") else 0.0,
                    o.get("payment_method", ""),
                    o.get("tracking_code", ""),
                    o.get("estimated_delivery", ""),
                    o.get("notes", ""),
                )
                for o in orders
            ],
        )

        items = self._read_rows("order_items")
        self.conn.executemany(
            "INSERT INTO order_items VALUES (?, ?, ?)",
            [
                (int(i["order_id"]), int(i["quantity"]), int(i["product_id"]))
                for i in items
            ],
        )

        promos = self._read_rows("promotions")
        self.conn.executemany(
            "INSERT INTO promotions VALUES (?, ?, ?, ?, ?)",
            [
                (
                    int(p["promotion_id"]),
                    int(p["product_id"]),
                    int(p["discount_percent"]),
                    p.get("description", ""),
                    int(p["is_active"]),
                )
                for p in promos
            ],
        )

        self.conn.commit()

    # ---------------------------------------------------------------- helpers
    def _promo_map(self) -> dict[int, dict[str, Any]]:
        """Best active promotion per product (highest discount wins)."""
        rows = self.conn.execute(
            "SELECT product_id, discount_percent, description "
            "FROM promotions WHERE is_active = 1"
        ).fetchall()
        best: dict[int, dict[str, Any]] = {}
        for row in rows:
            pid = row["product_id"]
            disc = row["discount_percent"]
            if pid not in best or disc > best[pid]["discount_percent"]:
                best[pid] = {
                    "discount_percent": disc,
                    "description": row["description"],
                }
        return best

    @staticmethod
    def _parse_specs(raw: str) -> dict[str, Any]:
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}

    def _product_to_dict(
        self,
        row: sqlite3.Row,
        promos: dict[int, dict[str, Any]],
        category_name: str | None,
    ) -> dict[str, Any]:
        price = float(row["price_brl"])
        promo = promos.get(row["product_id"])
        final_price = round(price * (1 - promo["discount_percent"] / 100), 2) if promo else price
        return {
            "product_id": row["product_id"],
            "name": row["name"],
            "price": price,
            "final_price": final_price,
            "category": category_name,
            "stock": int(row["stock_quantity"]),
            "status": row["status"],
            "description": row["description"],
            "specs": self._parse_specs(row["specs"]),
            "promotion": (
                {
                    "discount_percent": promo["discount_percent"],
                    "description": promo["description"],
                }
                if promo
                else None
            ),
        }

    # ---------------------------------------------------------------- queries
    def search_products(
        self,
        query: str | None = None,
        *,
        max_price: float | None = None,
        min_price: float | None = None,
        category: str | None = None,
        only_available: bool = True,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search the catalog with optional text, price range and category filters."""
        sql = (
            "SELECT p.*, c.name AS category_name FROM products p "
            "LEFT JOIN categories c ON c.category_id = p.category_id WHERE 1=1"
        )
        params: list[Any] = []

        if only_available:
            sql += " AND p.status = 'active' AND p.stock_quantity > 0"
        if max_price is not None:
            sql += " AND p.price_brl <= ?"
            params.append(float(max_price))
        if min_price is not None:
            sql += " AND p.price_brl >= ?"
            params.append(float(min_price))
        if category:
            sql += " AND c.name_norm LIKE ?"
            params.append(f"%{normalize(category)}%")
        if query:
            like = f"%{normalize(query)}%"
            sql += " AND (p.name_norm LIKE ? OR p.description_norm LIKE ? OR c.name_norm LIKE ?)"
            params.extend([like, like, like])

        sql += " ORDER BY p.price_brl ASC LIMIT ?"
        params.append(int(limit))

        rows = self.conn.execute(sql, params).fetchall()
        promos = self._promo_map()
        return [self._product_to_dict(r, promos, r["category_name"]) for r in rows]

    def get_product(
        self, *, product_id: int | None = None, name: str | None = None
    ) -> dict[str, Any] | None:
        """Fetch a single product by id or (partial) name."""
        base = (
            "SELECT p.*, c.name AS category_name FROM products p "
            "LEFT JOIN categories c ON c.category_id = p.category_id "
        )
        if product_id is not None:
            row = self.conn.execute(base + "WHERE p.product_id = ?", (int(product_id),)).fetchone()
        elif name:
            row = self.conn.execute(
                base + "WHERE p.name_norm LIKE ? ORDER BY p.price_brl ASC LIMIT 1",
                (f"%{normalize(name)}%",),
            ).fetchone()
        else:
            return None

        if row is None:
            return None
        return self._product_to_dict(row, self._promo_map(), row["category_name"])

    def all_products(self) -> list[dict[str, Any]]:
        """Return minimal product rows (used for fuzzy name matching)."""
        rows = self.conn.execute(
            "SELECT product_id, name, name_norm, price_brl, status, stock_quantity "
            "FROM products"
        ).fetchall()
        return [
            {
                "product_id": r["product_id"],
                "name": r["name"],
                "name_norm": r["name_norm"],
                "price": float(r["price_brl"]),
                "status": r["status"],
                "stock": int(r["stock_quantity"]),
            }
            for r in rows
        ]

    def get_order(
        self, *, order_id: int | None = None, tracking_code: str | None = None
    ) -> dict[str, Any] | None:
        """Fetch an order (with customer and items) by id or tracking code."""
        base = (
            "SELECT o.*, c.name AS customer_name, c.city AS customer_city "
            "FROM orders o LEFT JOIN customers c ON c.customer_id = o.customer_id "
        )
        if order_id is not None:
            row = self.conn.execute(base + "WHERE o.order_id = ?", (int(order_id),)).fetchone()
        elif tracking_code:
            row = self.conn.execute(
                base + "WHERE UPPER(REPLACE(o.tracking_code, ' ', '')) = UPPER(?)",
                (tracking_code.strip(),),
            ).fetchone()
        else:
            return None

        if row is None:
            return None

        item_rows = self.conn.execute(
            "SELECT oi.quantity, p.product_id, p.name, p.price_brl "
            "FROM order_items oi JOIN products p ON p.product_id = oi.product_id "
            "WHERE oi.order_id = ?",
            (row["order_id"],),
        ).fetchall()

        return {
            "order_id": row["order_id"],
            "customer_name": row["customer_name"],
            "customer_city": row["customer_city"],
            "order_date": row["order_date"],
            "status": row["status"],
            "total": float(row["total_brl"]),
            "payment_method": row["payment_method"],
            "tracking_code": row["tracking_code"],
            "estimated_delivery": row["estimated_delivery"],
            "notes": row["notes"],
            "items": [
                {
                    "product_id": it["product_id"],
                    "name": it["name"],
                    "quantity": it["quantity"],
                    "unit_price": float(it["price_brl"]),
                }
                for it in item_rows
            ],
        }

    def categories(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT category_id, name, description FROM categories ORDER BY category_id"
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self) -> None:
        self.conn.close()
