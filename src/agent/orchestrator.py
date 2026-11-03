"""Agent orchestrator.

Two interchangeable modes:

* **LLM mode** — uses an OpenAI-compatible model with function calling (tools)
  in a ReAct-style loop. Enabled when a usable ``LLM_API_KEY`` is configured.
* **Offline mode** — a deterministic, rule-based fallback that still calls the
  same tools. Enabled automatically when no key/`openai` package is available,
  so the agent is always runnable and testable.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from ..config import Settings, load_settings
from ..data.policies import POLICY_PDF_NAME, PolicyIndex
from ..data.store import DataStore
from ..data.text import normalize
from .prompt import SYSTEM_PROMPT
from .tools import TOOL_SPECS, StoreTools

logger = logging.getLogger(__name__)

MAX_MESSAGE_CHARS = 2000
MAX_HISTORY_MESSAGES = 20

_STOPWORDS = set(
    """the a an is are do does did you your i my me of for to please how much what
    which can could would have has it this that and or in on at with about there any
    some be am want need hi hello hey thanks thank quanto custa qual quais tem voces
    eu meu minha por favor de do da um uma o os as e ou no na em""".split()
)

# Category detection — order matters (specific before generic).
_CATEGORY_KEYWORDS: list[tuple[str, list[str]]] = [
    ("Violões", ["acoustic guitar", "acoustic", "violao", "violoes", "nylon"]),
    ("Guitarras", ["guitar", "guitars", "guitarra", "guitarras", "electric guitar"]),
    ("Baixos", ["bass", "basses", "baixo", "baixos"]),
    ("Baterias e Percussão", ["drum", "drums", "bateria", "baterias", "percussion", "percussao"]),
    ("Teclados e Pianos", ["keyboard", "keyboards", "teclado", "teclados", "piano", "pianos"]),
    (
        "Instrumentos de Sopro (Madeiras)",
        ["sax", "saxophone", "flute", "flauta", "clarinet", "woodwind"],
    ),
    ("Instrumentos de Sopro (Metais)", ["trumpet", "trombone", "brass", "trompete"]),
    ("Cordas Orquestrais", ["violin", "violino", "cello", "violoncelo", "orchestral"]),
    ("Ukuleles", ["ukulele", "ukelele"]),
]

_ACCESSORY_WORDS = set(
    """string strings corda cordas cabo cabos cable cables palheta palhetas reed reeds
    pedal pedais amplificador amplifiers amp amps case cases capa capas acessorio
    acessorios accessory accessories baqueta baquetas stick sticks""".split()
)

_PRICE_KEYWORDS = [
    "how much", "price", "cost", "quanto custa", "quanto e", "preco", "custa", "valor",
]
_SEARCH_KEYWORDS = [
    "which", "options", "quais", "opcoes", "show", "list", "looking for", "buscar",
    "procuro", "under", "below", "ate", "menos de", "do you have", "voces tem",
]
_STOCK_KEYWORDS = [
    "stock", "available", "availability", "in stock", "do you have", "have the",
    "disponivel", "estoque", "tem",
]
_CONTACT_KEYWORDS = [
    "address", "endereco", "where are you", "where is the store", "onde fica",
    "telefone", "phone", "contact", "contato", "email", "cnpj", "location", "whatsapp",
]
_POLICY_KEYWORDS = [
    "return", "returns", "refund", "exchange", "exchanges", "warranty", "payment", "pay",
    "installment", "installments", "pix", "boleto", "credit", "debit", "shipping",
    "delivery", "freight", "hours", "open", "close", "privacy", "lgpd", "policy",
    "policies", "rules", "troca", "trocas", "devolucao", "devolucoes", "devolver",
    "garantia", "pagamento", "frete", "entrega", "horario", "funcionamento",
    "privacidade", "parcel", "parcelamento", "desconto", "promotion", "promocao", "regras",
]

_GREETING_WORDS = {"hi", "hello", "hey", "oi", "ola", "bom", "boa", "good", "eai", "e"}


def _fmt_money(value: float) -> str:
    return f"R$ {value:,.2f}"


class Agent:
    """Stateful conversational agent (keeps an in-memory history)."""

    def __init__(
        self,
        settings: Settings | None = None,
        data_dir: str | None = None,
    ) -> None:
        self.settings = settings or load_settings()
        self.store = DataStore(data_dir)
        self.policies = PolicyIndex(self.store.data_dir / POLICY_PDF_NAME)
        self.tools = StoreTools(self.store, self.policies)
        self.history: list[dict[str, str]] = []
        self._last_product_id: int | None = None

    # ------------------------------------------------------------------ public
    @property
    def mode(self) -> str:
        return "llm" if self.settings.llm_enabled else "offline"

    def reset(self) -> None:
        self.history.clear()

    def chat(self, message: str) -> str:
        message = (message or "").strip()
        if not message:
            return "Hi! How can I help you today?"
        if len(message) > MAX_MESSAGE_CHARS:
            return (
                "That message is a bit long for me — could you summarize it in a few "
                "sentences so I can help you faster?"
            )

        self.history.append({"role": "user", "content": message})
        if self.settings.llm_enabled:
            try:
                reply = self._chat_llm()
            except Exception as exc:  # noqa: BLE001 - fall back gracefully
                logger.warning("LLM mode failed (%s); using offline mode", exc)
                reply = self._offline_respond(message)
        else:
            reply = self._offline_respond(message)

        self.history.append({"role": "assistant", "content": reply})
        return reply

    # ------------------------------------------------------------------- LLM
    def _chat_llm(self) -> str:
        from openai import OpenAI  # imported lazily so offline mode needs no extra dep

        client = OpenAI(
            api_key=self.settings.api_key,
            base_url=self.settings.base_url or None,
            # Some OpenAI SDK builds bundle an httpx variant whose gzip decoder is
            # broken ("process() takes no keyword arguments"). Asking for identity
            # encoding avoids that broken decompression path and is harmless otherwise.
            default_headers={"Accept-Encoding": "identity"},
        )
        recent = self.history[-MAX_HISTORY_MESSAGES:]
        messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            {"role": m["role"], "content": m["content"]} for m in recent
        ]

        for _ in range(6):
            response = client.chat.completions.create(
                model=self.settings.model,
                messages=messages,
                tools=TOOL_SPECS,
                tool_choice="auto",
                temperature=self.settings.temperature,
                max_tokens=self.settings.max_tokens,
            )
            msg = response.choices[0].message
            tool_calls = getattr(msg, "tool_calls", None)
            if not tool_calls:
                return (msg.content or "").strip()

            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in tool_calls
                    ],
                }
            )
            for tc in tool_calls:
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                result = self.tools.dispatch(tc.function.name, args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )

        return "Sorry, I couldn't complete that request. Could you try rephrasing?"

    # --------------------------------------------------------------- Offline
    def _offline_respond(self, message: str) -> str:
        norm = normalize(message)

        if self._is_greeting(norm):
            return (
                "Hey! Welcome to Empório da Música 🎶 I'm Lira, your virtual assistant. "
                "I can help with instruments, prices, stock, orders and store policies. "
                "What are you looking for?"
            )

        order_answer = self._try_order(message, norm)
        if order_answer is not None:
            return order_answer

        if self._is_accessory_request(norm):
            return self._out_of_scope()

        if self._has_any(norm, _CONTACT_KEYWORDS):
            return self._store_info_answer()

        if self._has_any(norm, _PRICE_KEYWORDS):
            product = self._match_product(message)
            if product is not None:
                return self._price_answer(product)
            search = self._category_search(message, norm)
            if search is not None:
                return search
            return (
                "I can help with prices! Which model are you interested in? For example, "
                "ask 'How much is the Takamine GD20?'."
            )

        if self._has_any(norm, _STOCK_KEYWORDS):
            product = self._match_product(message)
            if product is not None:
                return self._price_answer(product)

        search = self._category_search(message, norm)
        if search is not None:
            return search

        if self._has_any(norm, _POLICY_KEYWORDS):
            return self._policy_answer(message)

        results = self.policies.search(message, top_k=1)
        if results:
            return self._policy_answer(message)

        return (
            "I'm here to help with instruments, prices, stock, orders and store policies. "
            "Could you tell me a bit more about what you're looking for?"
        )

    # ---------------------------------------------------------- offline helpers
    @staticmethod
    def _has_any(norm: str, keywords: list[str]) -> bool:
        norm_tokens = set(norm.split())
        for keyword in keywords:
            k_norm = normalize(keyword)
            if not k_norm:
                continue
            if " " in k_norm:
                if k_norm in norm:
                    return True
            elif k_norm in norm_tokens:
                return True
        return False

    @staticmethod
    def _is_greeting(norm: str) -> bool:
        words = norm.split()
        if not words or len(words) > 5:
            return False
        return words[0] in _GREETING_WORDS and not any(
            w in _ACCESSORY_WORDS for w in words
        )

    def _is_accessory_request(self, norm: str) -> bool:
        tokens = set(norm.split())
        has_acc = bool(tokens & _ACCESSORY_WORDS)
        if not has_acc:
            return False
        intent = tokens & {
            "sell", "sells", "have", "buy", "vende", "tem", "quero", "preciso", "need",
            "want", "comprar", "procuro", "looking", "possui",
        }
        return bool(intent) or len(tokens) <= 3

    def _try_order(self, message: str, norm: str) -> str | None:
        tracking = re.search(r"\bBR[A-Z0-9]{9}BR\b", message.upper())
        mentions_order = self._has_any(norm, ["pedido", "order", "rastre", "track"])
        if not tracking and not mentions_order:
            return None

        if tracking:
            order = self.tools.get_order_status(tracking_code=tracking.group(0))["order"]
        else:
            number = re.search(r"\b(\d{1,5})\b", message)
            if not number:
                return (
                    "Sure! Please share your order number or tracking code "
                    "(it looks like BR123456789BR) so I can check it for you."
                )
            order = self.tools.get_order_status(order_id=int(number.group(1)))["order"]

        if order is None:
            if tracking:
                return (
                    "I couldn't find an order for that tracking code. Could you "
                    "double-check it? The format is BR + 9 characters + BR."
                )
            return (
                "I couldn't find an order with that number. Could you confirm the order "
                "id or share your tracking code?"
            )
        return self._order_answer(order)

    def _match_product(self, message: str) -> dict[str, Any] | None:
        query_tokens = {
            t
            for t in normalize(message).split()
            if t not in _STOPWORDS and len(t) >= 2
        }
        best_id: int | None = None
        best_score = 0
        for product in self.store.all_products():
            name_tokens = {
                t for t in product["name_norm"].split() if t not in _STOPWORDS
            }
            overlap = query_tokens & name_tokens
            score = sum(len(t) for t in overlap)
            if score > best_score:
                best_score = score
                best_id = product["product_id"]

        if best_id is not None and best_score >= 4:
            self._last_product_id = best_id
            return self.store.get_product(product_id=best_id)

        # Follow-up questions like "Do you have it in stock?" refer to the last product.
        pronoun = re.search(
            r"\b(it|this|that|these|those|desse|dele|dessa|dela|esse|essa|isso)\b",
            normalize(message),
        )
        if self._last_product_id is not None and pronoun:
            return self.store.get_product(product_id=self._last_product_id)
        return None

    @staticmethod
    def _detect_category(norm: str) -> str | None:
        for category, keywords in _CATEGORY_KEYWORDS:
            if any(normalize(k) in norm for k in keywords):
                return category
        return None

    @staticmethod
    def _parse_max_price(message: str) -> float | None:
        match = re.search(r"R\$\s*([\d\.]+(?:,\d{2})?)", message, re.I)
        if not match:
            match = re.search(
                r"(?:under|below|less than|ate|menos de|up to|max|maximo)\s*(?:r\s*)?(\d[\d\.]*)",
                normalize(message),
            )
        if not match:
            return None
        raw = match.group(1).replace(".", "").replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            return None

    def _category_search(self, message: str, norm: str) -> str | None:
        category = self._detect_category(norm)
        max_price = self._parse_max_price(message)
        has_search_hint = self._has_any(norm, _SEARCH_KEYWORDS)
        if category is None and max_price is None:
            return None
        if category is None and not has_search_hint:
            return None

        products = self.store.search_products(
            category=category, max_price=max_price, only_available=True, limit=8
        )
        if not products:
            return (
                "I couldn't find available instruments for that filter. Want to try a "
                "different category or budget?"
            )
        return self._format_product_list(products, category, max_price)

    def _format_product_list(
        self, products: list[dict[str, Any]], category: str | None, max_price: float | None
    ) -> str:
        header = "Here are some options"
        if category:
            header += f" in {category}"
        if max_price is not None:
            header += f" up to {_fmt_money(max_price)}"
        header += ":"

        lines = []
        for p in products:
            line = f"• {p['name']} — {_fmt_money(p['price'])}"
            if p.get("promotion"):
                promo = p["promotion"]
                line += (
                    f" (promo {promo['discount_percent']}% off: {_fmt_money(p['final_price'])})"
                )
            line += f" · {p['stock']} in stock"
            lines.append(line)
        return header + "\n" + "\n".join(lines) + "\n\nWant more details on any of these?"

    def _price_answer(self, product: dict[str, Any]) -> str:
        name = product["name"]
        price = product["price"]
        parts = [f"The {name} is {_fmt_money(price)}."]

        if product["status"] == "discontinued":
            parts.append("Heads up: this model has been discontinued, but I can suggest a successor.")
        elif product["status"] == "coming_soon":
            parts.append("It's coming soon to our catalog.")
        elif product["stock"] == 0:
            parts.append("It's currently out of stock — want me to suggest similar options?")
        else:
            parts.append(f"It's in stock ({product['stock']} units available).")

        if product.get("promotion"):
            promo = product["promotion"]
            parts.append(
                f"It's on promotion: {promo['discount_percent']}% off "
                f"(from {_fmt_money(price)} to {_fmt_money(product['final_price'])})."
            )
        elif product["status"] == "active" and product["stock"] > 0:
            parts.append("PIX payments get an extra 5% off the list price.")
        return " ".join(parts)

    @staticmethod
    def _order_answer(order: dict[str, Any]) -> str:
        parts = [f"Order #{order['order_id']} is currently '{order['status']}'."]
        if order.get("estimated_delivery"):
            parts.append(f"Estimated delivery: {order['estimated_delivery']}.")
        if order.get("tracking_code"):
            parts.append(f"Tracking code: {order['tracking_code']}.")
        parts.append(f"Total: {_fmt_money(order['total'])}.")
        if order.get("items"):
            items = ", ".join(f"{i['quantity']}x {i['name']}" for i in order["items"])
            parts.append(f"Items: {items}.")
        return " ".join(parts)

    def _policy_answer(self, question: str) -> str:
        results = self.tools.query_policies(question)["results"]
        if not results:
            return (
                "I'm not totally sure about that policy. Could you rephrase it? "
                "I can also connect you with our team."
            )
        return results[0]["answer"]

    def _store_info_answer(self) -> str:
        info = self.tools.get_store_info()
        return (
            f"You can find us at {info['address']}. "
            f"Phone/WhatsApp: {info['phone_whatsapp']}. Email: {info['email']}. "
            "Hours: Mon–Fri 09:00–18:00, Sat 09:00–13:00, closed Sundays and holidays."
        )

    @staticmethod
    def _out_of_scope() -> str:
        return (
            "Great question! We're a musical-instrument store, so we don't carry accessories "
            "like strings, cables, reeds, pedals, amps or cases. I'd be glad to help you find "
            "an instrument, though — and for accessories I recommend checking a partner store."
        )

    def close(self) -> None:
        self.store.close()
