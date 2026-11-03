"""Tests for the policy extraction and keyword retrieval."""

from __future__ import annotations

from src.data.policies import PolicyIndex, extract_sections


def test_extract_sections_from_pdf(store) -> None:  # noqa: ANN001
    sections = extract_sections(store.data_dir / "políticas_da_loja.pdf")
    assert "about" in sections
    assert "returns" in sections
    assert "shipping" in sections
    assert "Empório da Música" in sections["about"]


def test_search_return_policy(policies: PolicyIndex) -> None:
    results = policies.search("Can I return a product I changed my mind about?")
    assert results
    assert results[0]["id"] == "returns"


def test_search_business_hours(policies: PolicyIndex) -> None:
    results = policies.search("What are your business hours?")
    assert results
    assert results[0]["id"] == "hours"


def test_search_pix_payment(policies: PolicyIndex) -> None:
    ids = [r["id"] for r in policies.search("Do you accept PIX?")]
    assert "payment" in ids


def test_search_shipping(policies: PolicyIndex) -> None:
    results = policies.search("How long does delivery take to another city?")
    assert results
    assert results[0]["id"] == "shipping"
