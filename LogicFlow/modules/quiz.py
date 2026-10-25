"""In-memory quiz question bank and scoring helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Question:
    id: str
    topic: str
    qtype: str  # "mcq" or "numerical"
    prompt: str
    options: list[str] | None
    answer: str
    explanation: str


QUESTION_BANK: list[Question] = [
    Question(
        id="g1",
        topic="Logic Gates",
        qtype="mcq",
        prompt="What is the output of a 2-input AND gate when A=1 and B=0?",
        options=["0", "1", "High-Z", "Undefined"],
        answer="0",
        explanation="AND is 1 only when both inputs are 1. 1 AND 0 = 0.",
    ),
    Question(
        id="g2",
        topic="Logic Gates",
        qtype="mcq",
        prompt="Which gate is known as a universal gate?",
        options=["XOR", "OR", "NAND", "XNOR"],
        answer="NAND",
        explanation="NAND (and NOR) are functionally complete — any Boolean function can be built from them.",
    ),
    Question(
        id="g3",
        topic="Logic Gates",
        qtype="mcq",
        prompt="XOR output is 1 when:",
        options=["Both inputs are 1", "Both inputs are 0", "Inputs are different", "Always"],
        answer="Inputs are different",
        explanation="XOR detects inequality of the two inputs.",
    ),
    Question(
        id="g4",
        topic="Logic Gates",
        qtype="numerical",
        prompt="For inputs A=1, B=1, what is the decimal output (0 or 1) of NAND?",
        options=None,
        answer="0",
        explanation="NAND(1,1) = NOT(1) = 0.",
    ),
    Question(
        id="b1",
        topic="Boolean Algebra",
        qtype="mcq",
        prompt="Which law states A + A·B = A?",
        options=["De Morgan's", "Absorption", "Commutative", "Associative"],
        answer="Absorption",
        explanation="Absorption law: A + A·B = A and A·(A+B) = A.",
    ),
    Question(
        id="b2",
        topic="Boolean Algebra",
        qtype="mcq",
        prompt="De Morgan's theorem: (A·B)' equals:",
        options=["A'·B'", "A'+B'", "A·B", "A+B"],
        answer="A'+B'",
        explanation="(A·B)' = A' + B' and (A+B)' = A'·B'.",
    ),
    Question(
        id="b3",
        topic="Boolean Algebra",
        qtype="mcq",
        prompt="SOP stands for:",
        options=[
            "Sum of Products",
            "System of Processors",
            "Signal Output Path",
            "Series of Pulses",
        ],
        answer="Sum of Products",
        explanation="Sum-of-Products is an OR of AND terms (minterm expansion).",
    ),
    Question(
        id="b4",
        topic="Boolean Algebra",
        qtype="numerical",
        prompt="Simplify A+1. Enter the result as 0 or 1.",
        options=None,
        answer="1",
        explanation="OR with 1 is always 1 (Annulment / Dominance law).",
    ),
    Question(
        id="k1",
        topic="Karnaugh Maps",
        qtype="mcq",
        prompt="A 3-variable K-map has how many cells?",
        options=["4", "6", "8", "16"],
        answer="8",
        explanation="2³ = 8 cells, one per minterm.",
    ),
    Question(
        id="k2",
        topic="Karnaugh Maps",
        qtype="mcq",
        prompt="Valid K-map group sizes are powers of two. Which size is invalid?",
        options=["1", "2", "3", "4"],
        answer="3",
        explanation="Groups must contain 1, 2, 4, 8, … cells — not 3.",
    ),
    Question(
        id="k3",
        topic="Karnaugh Maps",
        qtype="mcq",
        prompt="Adjacent cells in a K-map differ by how many bits?",
        options=["0", "1", "2", "All bits"],
        answer="1",
        explanation="Gray-code adjacency means exactly one bit changes between neighbors (including wrap-around).",
    ),
    Question(
        id="k4",
        topic="Karnaugh Maps",
        qtype="numerical",
        prompt="How many variables does a 16-cell K-map represent?",
        options=None,
        answer="4",
        explanation="2⁴ = 16 cells → 4 variables.",
    ),
    Question(
        id="d1",
        topic="Number Systems & Basics",
        qtype="mcq",
        prompt="A minterm is a product term that is 1 for:",
        options=[
            "Exactly one input combination",
            "All input combinations",
            "No input combinations",
            "Don't-care cases only",
        ],
        answer="Exactly one input combination",
        explanation="Each minterm corresponds to one row of the truth table where F=1.",
    ),
    Question(
        id="d2",
        topic="Number Systems & Basics",
        qtype="mcq",
        prompt="POS means:",
        options=[
            "Product of Sums",
            "Power of Signals",
            "Parallel Output Switch",
            "Positive Output State",
        ],
        answer="Product of Sums",
        explanation="Product-of-Sums is an AND of OR terms (maxterm expansion).",
    ),
]


TOPICS = sorted({q.topic for q in QUESTION_BANK})


def get_questions(topic: str | None = None) -> list[Question]:
    if topic is None or topic == "All Topics":
        return list(QUESTION_BANK)
    return [q for q in QUESTION_BANK if q.topic == topic]


def check_answer(question: Question, user_answer: str) -> bool:
    return user_answer.strip().lower() == question.answer.strip().lower()


def score_quiz(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    correct = sum(1 for r in results if r.get("correct"))
    pct = round(100.0 * correct / total, 1) if total else 0.0
    return {"total": total, "correct": correct, "percent": pct}
