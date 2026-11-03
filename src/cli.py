"""Command-line interface for the Empório da Música agent.

Usage:
    python -m src.cli                     # interactive chat
    python -m src.cli -m "How much is the Takamine GD20?"
    python -m src.cli --offline -m "..."  # force the deterministic offline mode
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
import sys

from .agent import Agent
from .config import load_settings


def _build_agent(args: argparse.Namespace) -> Agent:
    settings = load_settings()
    if args.offline:
        settings = dataclasses.replace(settings, api_key=None)
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(levelname)s %(name)s: %(message)s",
    )
    return Agent(settings=settings, data_dir=args.data_dir)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="emporio-agent",
        description="Empório da Música customer service agent (CLI).",
    )
    parser.add_argument("-m", "--message", help="Send a single message and exit.")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Force deterministic offline mode (no LLM/API key needed).",
    )
    parser.add_argument("--data-dir", default=None, help="Override the data directory.")
    args = parser.parse_args(argv)

    agent = _build_agent(args)
    try:
        if args.message:
            print(agent.chat(args.message))
            return 0
        _interactive(agent)
        return 0
    finally:
        agent.close()


def _interactive(agent: Agent) -> None:
    print("=" * 60)
    print(" Empório da Música — virtual assistant (type /quit to exit)")
    print(f" Mode: {agent.mode}")
    print("=" * 60)
    while True:
        try:
            user = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye! 🎶")
            break
        if user.lower() in {"/quit", "/exit", "quit", "exit"}:
            print("Bye! 🎶")
            break
        if user.lower() == "/reset":
            agent.reset()
            print("(conversation reset)")
            continue
        if user.lower() == "/help":
            print("Commands: /reset (clear history), /quit (exit).")
            continue
        if not user:
            continue
        print(f"Lira: {agent.chat(user)}")


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
