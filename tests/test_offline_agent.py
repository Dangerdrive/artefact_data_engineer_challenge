"""Tests for the deterministic offline agent behavior."""

from __future__ import annotations

from src.agent import Agent


def test_mode_is_offline(agent: Agent) -> None:
    assert agent.mode == "offline"


def test_price_query(agent: Agent) -> None:
    reply = agent.chat("How much is the Takamine GD20?")
    assert "Takamine" in reply
    assert "2,199.00" in reply


def test_catalog_search_query(agent: Agent) -> None:
    reply = agent.chat("Which acoustic guitars do you have under R$1000?")
    assert "Violões" in reply
    assert "R$" in reply


def test_order_tracking_query(agent: Agent) -> None:
    reply = agent.chat("Where is my order? The code is BRAB1234567BR")
    assert "delivered" in reply
    assert "BRAB1234567BR" in reply


def test_return_policy_query(agent: Agent) -> None:
    reply = agent.chat("I changed my mind about my purchase, can I return it?")
    assert "7 calendar days" in reply


def test_out_of_scope_accessory_query(agent: Agent) -> None:
    reply = agent.chat("Do you sell guitar strings?")
    assert "accessories" in reply.lower()


def test_out_of_stock_query(agent: Agent) -> None:
    reply = agent.chat("Do you have the Giannini GF-3D in stock?")
    assert "out of stock" in reply.lower()


def test_greeting(agent: Agent) -> None:
    reply = agent.chat("hello")
    assert "Empório" in reply or "Lira" in reply


def test_conversation_history_is_tracked(agent: Agent) -> None:
    agent.chat("hi")
    agent.chat("How much is the Takamine GD20?")
    assert len(agent.history) == 4
    assert agent.history[0]["role"] == "user"
    assert agent.history[-1]["role"] == "assistant"


def test_pronoun_followup_uses_previous_product(agent: Agent) -> None:
    agent.chat("How much is the Takamine GD20?")
    reply = agent.chat("Do you have it in stock?")
    assert "Takamine GD20" in reply


def test_very_long_message_is_guarded(agent: Agent) -> None:
    reply = agent.chat("x" * 5000)
    assert "long" in reply.lower() or "summarize" in reply.lower()


def test_purchase_intent_is_not_treated_as_order_status(agent: Agent) -> None:
    reply = agent.chat("I want to order 2 guitars")
    assert "Order #" not in reply
    assert "delivered" not in reply


def test_portuguese_policy_answer(agent: Agent) -> None:
    reply = agent.chat("Qual é o horário de funcionamento?")
    assert "segunda" in reply
