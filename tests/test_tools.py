"""Tests for the agent tools and their dispatch."""

from __future__ import annotations

from src.agent.tools import StoreTools
from src.data.policies import PolicyIndex
from src.data.store import DataStore


def _tools(store: DataStore, policies: PolicyIndex) -> StoreTools:
    return StoreTools(store, policies)


def test_search_products_tool(store: DataStore, policies: PolicyIndex) -> None:
    result = _tools(store, policies).search_products(category="Violões", max_price=1000)
    assert result["count"] > 0
    assert all(p["price"] <= 1000 for p in result["products"])


def test_get_product_tool(store: DataStore, policies: PolicyIndex) -> None:
    result = _tools(store, policies).get_product(name="Takamine GD20")
    assert result["found"] is True
    assert "Takamine" in result["product"]["name"]


def test_order_status_tool(store: DataStore, policies: PolicyIndex) -> None:
    result = _tools(store, policies).get_order_status(tracking_code="BRAB1234567BR")
    assert result["found"] is True
    assert result["order"]["status"] == "delivered"


def test_query_policies_tool(store: DataStore, policies: PolicyIndex) -> None:
    result = _tools(store, policies).query_policies("what are the business hours?")
    assert result["found"] is True
    assert result["results"][0]["id"] == "hours"


def test_calc_shipping_campo_grande_free(store: DataStore, policies: PolicyIndex) -> None:
    result = _tools(store, policies).calc_shipping("Campo Grande", 600)
    assert result["free_shipping"] is True
    assert result["cost"] == 0.0


def test_calc_shipping_campo_grande_paid(store: DataStore, policies: PolicyIndex) -> None:
    result = _tools(store, policies).calc_shipping("Campo Grande", 100)
    assert result["free_shipping"] is False
    assert result["cost"] == 35.0


def test_calc_shipping_other_city(store: DataStore, policies: PolicyIndex) -> None:
    result = _tools(store, policies).calc_shipping("Dourados", 100)
    assert result["cost"] is None
    assert len(result["options"]) == 3


def test_store_info_tool(store: DataStore, policies: PolicyIndex) -> None:
    info = _tools(store, policies).get_store_info()
    assert info["name"] == "Empório da Música"
    assert "Campo Grande" in info["address"]


def test_dispatch_unknown_tool(store: DataStore, policies: PolicyIndex) -> None:
    result = _tools(store, policies).dispatch("does_not_exist", {})
    assert "error" in result
