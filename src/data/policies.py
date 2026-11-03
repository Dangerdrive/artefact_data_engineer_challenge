"""Policy knowledge base and retrieval.

The source of truth is the store's policies manual (``políticas_da_loja.pdf``).
We extract the manual text (to quote the source) and pair it with a compact,
bilingual keyword index so retrieval works for both English and Portuguese
questions. Each entry carries a concise English answer used by the offline mode;
the LLM mode can additionally quote the extracted source excerpt.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .text import normalize, tokens

POLICY_PDF_NAME = "políticas_da_loja.pdf"

# (section id, exact header as it appears in the manual)
SECTION_HEADERS: list[tuple[str, str]] = [
    ("about", "1. Sobre a Empório da Música"),
    ("hours", "2. Horário de Funcionamento"),
    ("payment", "3. Formas de Pagamento"),
    ("returns", "4. Política de Trocas e Devoluções"),
    ("shipping", "5. Política de Frete e Entregas"),
    ("promotions", "6. Promoções e Descontos"),
    ("service", "7. Atendimento via WhatsApp"),
    ("warranty", "8. Garantia"),
    ("privacy", "9. Privacidade e Proteção de Dados"),
    ("final", "10. Disposições Finais"),
]

# Compact, bilingual knowledge base (answers in English).
POLICY_KB: list[dict[str, Any]] = [
    {
        "id": "about",
        "title": "Store details and contact",
        "keywords": [
            "about", "who are you", "store", "company", "founded", "history",
            "contact", "phone", "email", "address", "where are you", "cnpj",
            "telefone", "contato", "endereco", "onde fica", "loja", "empresa",
            "sobre", "horario de funcionamento",
        ],
        "answer": (
            "Empório da Música is a musical-instrument store founded in 2008 in "
            "Campo Grande/MS. Address: Rua 14 de Maio, 3200 — Centro, Campo Grande-MS "
            "(ZIP 79202-333). Phone/WhatsApp: (67) 3341-4444. Email: "
            "contato@emporiodamusica.com.br. We sell exclusively musical instruments "
            "(guitars, basses, acoustic guitars, drums, keyboards, winds, orchestral "
            "strings and ukuleles)."
        ),
    },
    {
        "id": "hours",
        "title": "Business hours",
        "keywords": [
            "hours", "open", "close", "opening", "business hours", "what time",
            "saturday", "sunday", "holiday", "horario", "funcionamento", "aberto",
            "fechado", "sabado", "domingo", "feriado", "que horas", "expediente",
        ],
        "answer": (
            "Our hours are Monday to Friday, 09:00–18:00; Saturday, 09:00–13:00; "
            "closed on Sundays and holidays. On special dates (Black Friday, store "
            "anniversary, Christmas) hours may be extended, announced on social media."
        ),
    },
    {
        "id": "payment",
        "title": "Payment methods and installments",
        "keywords": [
            "payment", "pay", "pix", "credit card", "debit", "boleto", "installment",
            "installments", "parcel", "parcelamento", "desconto pix", "cartao",
            "formas de pagamento", "credito", "debito", "how can i pay",
        ],
        "answer": (
            "We accept PIX (5% off the list price), debit card, credit card (up to 12x "
            "interest-free) and bank slip (boleto). Installments: up to 3x with no "
            "minimum (except below R$50); 4x–6x with a R$80 minimum per installment; "
            "7x–12x with a R$100 minimum. Combined payment methods are allowed for "
            "purchases above R$2,000."
        ),
    },
    {
        "id": "returns",
        "title": "Returns and exchanges",
        "keywords": [
            "return", "refund", "exchange", "withdrawal", "change my mind", "regret",
            "troca", "devolucao", "devolver", "arrependimento", "defeito", "reembolso",
            "7 days", "30 days", "can i return",
        ],
        "answer": (
            "Online purchases can be returned within 7 calendar days of receipt (right "
            "of withdrawal), in the original packaging; the refund goes back to the "
            "original payment method within 10 business days and return shipping is on "
            "us. Defective products can be exchanged within 30 calendar days. Exchanges "
            "by preference (color/model/size) are allowed within 7 days, subject to "
            "availability. Custom-made items, 'final sale' items and wind mouthpieces "
            "cannot be exchanged."
        ),
    },
    {
        "id": "shipping",
        "title": "Shipping and delivery",
        "keywords": [
            "shipping", "delivery", "freight", "frete", "entrega", "correios", "sedex",
            "pac", "jadlog", "tracking", "rastreamento", "rastreio", "prazo", "cep",
            "when will it arrive", "shipping time",
        ],
        "answer": (
            "In the Campo Grande metropolitan region, shipping is free above R$500, "
            "otherwise a flat R$35, delivered in 1–3 business days by our own courier. "
            "For other cities we ship via Correios PAC (5–12 days), SEDEX (2–5 days) or "
            "Jadlog (3–8 days), all with tracking and insurance. Cost is calculated by "
            "destination ZIP, weight and dimensions. The tracking code looks like "
            "BR + 9 characters + BR (e.g., BR4K7M2X9P1BR)."
        ),
    },
    {
        "id": "promotions",
        "title": "Promotions and discounts",
        "keywords": [
            "promotion", "discount", "promo", "desconto", "promocao", "black friday",
            "cumulative", "cumulativo", "sale", "oferta", "aniversario", "queima de estoque",
        ],
        "answer": (
            "Promotions are periodic (anniversary in August, Black Friday in November, "
            "Back to School in February, Stock Clearance, Musician's Week). They are not "
            "cumulative, and the 5% PIX discount does not apply on top of promotional "
            "prices. Promotional prices are always shown with the original price and the "
            "discount percentage. Sold-out promo items get no rain check."
        ),
    },
    {
        "id": "service",
        "title": "Customer service and scope",
        "keywords": [
            "whatsapp", "attendance", "customer service", "atendimento", "response time",
            "out of scope", "scope", "accessories", "acessorios", "tom de voz", "tone",
            "fora do escopo", "do you sell",
        ],
        "answer": (
            "Our WhatsApp support uses a warm, informal-but-professional tone with "
            "replies within 5 minutes during business hours. We only sell musical "
            "instruments, so we don't carry accessories such as strings, cables, reeds, "
            "pedals, amps or cases — we'll happily point you to a partner store instead. "
            "For complaints we listen, log the issue and follow up within 24 business hours."
        ),
    },
    {
        "id": "warranty",
        "title": "Warranty",
        "keywords": [
            "warranty", "garantia", "defect", "defeito", "fabricante", "manufacturer",
            "covered", "cobertura",
        ],
        "answer": (
            "Every product has a 90-day legal warranty against manufacturing defects from "
            "the receipt date, plus the manufacturer's warranty (6 months to 2 years, per "
            "the certificate). It does not cover natural wear (frets, strings, felt, reeds), "
            "misuse/drops/extreme exposure, unauthorized repairs or cosmetic damage without "
            "functional impact."
        ),
    },
    {
        "id": "privacy",
        "title": "Privacy and LGPD",
        "keywords": [
            "privacy", "lgpd", "data protection", "personal data", "privacidade",
            "dados pessoais", "my data",
        ],
        "answer": (
            "We comply with Brazil's LGPD. Personal data is used only to process/deliver "
            "orders, communicate status/tracking, send promotions (with consent) and meet "
            "legal obligations. We don't share customer data with third parties for "
            "marketing, and you can request deletion of your data at any time."
        ),
    },
    {
        "id": "final",
        "title": "Final provisions",
        "keywords": [
            "final provisions", "disposicoes", "updates", "management", "gerencia",
            "policy changes",
        ],
        "answer": (
            "The manual is an internal reference for the service team (including the "
            "virtual assistant) and is updated periodically. When in doubt about a policy, "
            "the team consults management before answering the customer."
        ),
    },
]

# Portuguese answers for the offline mode (mirrors POLICY_KB).
POLICY_KB_PT: dict[str, str] = {
    "about": (
        "A Empório da Música é uma loja de instrumentos musicais fundada em 2008 em "
        "Campo Grande/MS. Endereço: Rua 14 de Maio, 3200 — Centro, Campo Grande-MS "
        "(CEP 79202-333). Telefone/WhatsApp: (67) 3341-4444. E-mail: "
        "contato@emporiodamusica.com.br. Vendemos exclusivamente instrumentos musicais "
        "(guitarras, baixos, violões, baterias, teclados, sopros, cordas orquestrais e "
        "ukuleles)."
    ),
    "hours": (
        "Nosso horário é de segunda a sexta, das 09:00 às 18:00; sábado, das 09:00 às "
        "13:00; fechado aos domingos e feriados. Em datas especiais (Black Friday, "
        "aniversário da loja, Natal) o horário pode ser estendido, divulgado nas redes "
        "sociais."
    ),
    "payment": (
        "Aceitamos PIX (5% de desconto sobre o preço de tabela), cartão de débito, cartão "
        "de crédito (até 12x sem juros) e boleto. Parcelamento: até 3x sem valor mínimo "
        "(exceto parcelas abaixo de R$ 50); de 4x a 6x com parcela mínima de R$ 80; de 7x "
        "a 12x com parcela mínima de R$ 100. Pagamentos combinados são permitidos em "
        "compras acima de R$ 2.000."
    ),
    "returns": (
        "Compras online podem ser devolvidas em até 7 dias corridos após o recebimento "
        "(direito de arrependimento), na embalagem original; o reembolso é feito pelo "
        "mesmo meio de pagamento em até 10 dias úteis e o frete da devolução é por nossa "
        "conta. Produtos com defeito podem ser trocados em até 30 dias corridos. Trocas "
        "por preferência (cor/modelo/tamanho) são permitidas em até 7 dias, sujeitas à "
        "disponibilidade. Itens personalizados, itens de 'venda final' e boquilhas de "
        "instrumentos de sopro não podem ser trocados."
    ),
    "shipping": (
        "Na região metropolitana de Campo Grande, o frete é grátis acima de R$ 500; abaixo "
        "disso, taxa fixa de R$ 35, com entrega em 1 a 3 dias úteis pela nossa própria "
        "entrega. Para outras cidades, enviamos por Correios PAC (5–12 dias), SEDEX "
        "(2–5 dias) ou Jadlog (3–8 dias), todos com rastreio e seguro. O custo é calculado "
        "pelo CEP de destino, peso e dimensões. O código de rastreio tem o formato BR + 9 "
        "caracteres + BR (ex.: BR4K7M2X9P1BR)."
    ),
    "promotions": (
        "As promoções são periódicas (aniversário em agosto, Black Friday em novembro, "
        "Volta às Aulas em fevereiro, Queima de Estoque, Semana do Músico). Elas não são "
        "cumulativas e o desconto de 5% do PIX não se aplica sobre preços promocionais. "
        "O preço promocional é sempre exibido junto com o preço original e o percentual "
        "de desconto. Itens esgotados em promoção não geram vale de reposição."
    ),
    "service": (
        "Nosso atendimento pelo WhatsApp usa um tom acolhedor, informal e profissional, "
        "com respostas em até 5 minutos em horário comercial. Vendemos somente "
        "instrumentos musicais, então não trabalhamos com acessórios como cordas, cabos, "
        "palhetas, pedais, amplificadores ou cases — indicamos com prazer uma loja "
        "parceira. Para reclamações, ouvimos, registramos e retornamos em até 24 horas "
        "úteis."
    ),
    "warranty": (
        "Todo produto tem garantia legal de 90 dias contra defeitos de fabricação a partir "
        "do recebimento, além da garantia do fabricante (6 meses a 2 anos, conforme o "
        "certificado). A garantia não cobre desgaste natural (trastes, cordas, feltros, "
        "palhetas), mau uso/quedas/exposição extrema, reparos não autorizados ou danos "
        "estéticos sem impacto funcional."
    ),
    "privacy": (
        "Seguimos a LGPD. Os dados pessoais são usados apenas para processar/entregar "
        "pedidos, comunicar status/rastreio, enviar promoções (com consentimento) e "
        "cumprir obrigações legais. Não compartilhamos seus dados com terceiros para "
        "marketing, e você pode solicitar a exclusão dos seus dados a qualquer momento."
    ),
    "final": (
        "O manual é uma referência interna da equipe de atendimento (incluindo o "
        "assistente virtual) e é atualizado periodicamente. Em caso de dúvida sobre uma "
        "política, a equipe consulta a gerência antes de responder ao cliente."
    ),
}


def _read_pdf_text(pdf_path: str | Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(re.sub(r"\s+", " ", text).strip())
    return " ".join(pages)


def _clean(text: str) -> str:
    text = re.sub(r"\d*\.?\s*Página\s*\d+", " ", text)
    text = text.replace("Empório da Música Manual de Políticas e Procedimentos", " ")
    return re.sub(r"\s+", " ", text).strip()


def extract_sections(pdf_path: str | Path) -> dict[str, str]:
    """Split the manual into sections keyed by section id."""
    text = _clean(_read_pdf_text(pdf_path))

    positions: list[tuple[int, str]] = []
    for section_id, header in SECTION_HEADERS:
        idx = text.find(header)
        if idx >= 0:
            positions.append((idx, section_id))
    positions.sort()

    sections: dict[str, str] = {}
    for i, (start, section_id) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        sections[section_id] = text[start:end].strip()
    return sections


class PolicyIndex:
    """Keyword-based retriever over the policy knowledge base."""

    def __init__(self, pdf_path: str | Path | None = None) -> None:
        self.source_sections: dict[str, str] = {}
        if pdf_path is not None and Path(pdf_path).exists():
            try:
                self.source_sections = extract_sections(pdf_path)
            except Exception:  # pragma: no cover - defensive: retrieval still works
                self.source_sections = {}

    def search(self, question: str, top_k: int = 2) -> list[dict[str, Any]]:
        """Return the most relevant policy entries for ``question`` (best first)."""
        q_norm = normalize(question)
        q_tokens = tokens(question)
        if not q_norm:
            return []

        scored: list[tuple[int, dict[str, Any]]] = []
        for entry in POLICY_KB:
            score = 0
            for keyword in entry["keywords"]:
                k_norm = normalize(keyword)
                if not k_norm:
                    continue
                if " " in k_norm:  # multi-word phrase
                    if k_norm in q_norm:
                        score += 3
                elif k_norm in q_tokens:
                    score += 2
            if score > 0:
                scored.append((score, entry))

        scored.sort(key=lambda item: item[0], reverse=True)

        results: list[dict[str, Any]] = []
        for score, entry in scored[:top_k]:
            results.append(
                {
                    "id": entry["id"],
                    "title": entry["title"],
                    "answer": entry["answer"],
                    "answer_pt": POLICY_KB_PT.get(entry["id"], entry["answer"]),
                    "source_excerpt": self.source_sections.get(entry["id"], "")[:600],
                    "score": score,
                }
            )
        return results
