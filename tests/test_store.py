"""Tests for the SQLite data store / query helpers."""

from __future__ import annotations

from src.data.store import DataStore


def test_search_acoustic_guitars_under_1000(store: DataStore) -> None:
    products = store.search_products(category="Violões", max_price=1000)
    assert products, "expected some acoustic guitars under R$1000"
    for product in products:
        assert product["category"] == "Violões"
        assert product["price"] <= 1000
        assert product["stock"] > 0
        assert product["status"] == "active"


def test_get_product_by_id(store: DataStore) -> None:
    product = store.get_product(product_id=95)
    assert product is not None
    assert "Takamine GD20" in product["name"]
    assert product["price"] == 2199.0


def test_get_product_by_name(store: DataStore) -> None:
    product = store.get_product(name="Takamine GD20")
    assert product is not None
    assert product["product_id"] == 95


def test_active_promotion_is_applied(store: DataStore) -> None:
    product = store.get_product(product_id=94)  # Taylor 110e, 8% active promo
    assert product is not None
    assert product["promotion"] is not None
    assert product["promotion"]["discount_percent"] == 8
    assert product["final_price"] == round(product["price"] * 0.92, 2)


def test_get_order_by_tracking_code(store: DataStore) -> None:
    order = store.get_order(tracking_code="BRAB1234567BR")
    assert order is not None
    assert order["order_id"] == 1
    assert order["status"] == "delivered"
    assert order["tracking_code"] == "BRAB1234567BR"


def test_get_order_by_id_includes_items(store: DataStore) -> None:
    order = store.get_order(order_id=1)
    assert order is not None
    assert len(order["items"]) == 1
    assert order["items"][0]["product_id"] == 93


def test_out_of_stock_product_is_flagged(store: DataStore) -> None:
    product = store.get_product(product_id=96)  # Giannini GF-3D, active, stock 0
    assert product is not None
    assert product["stock"] == 0
