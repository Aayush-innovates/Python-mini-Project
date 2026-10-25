"""Logic gate operations — pure Python, no Streamlit dependency."""

from __future__ import annotations

from typing import Callable

GateFn = Callable[..., int]

GATES: dict[str, dict] = {
    "AND": {
        "inputs": 2,
        "fn": lambda a, b: int(bool(a) and bool(b)),
        "symbol": "·",
        "expression": "Y = A · B",
        "description": (
            "AND outputs 1 only when every input is 1. "
            "It is the fundamental conjunction operation in digital logic."
        ),
    },
    "OR": {
        "inputs": 2,
        "fn": lambda a, b: int(bool(a) or bool(b)),
        "symbol": "+",
        "expression": "Y = A + B",
        "symbol_note": "+ denotes OR in Boolean algebra",
        "description": (
            "OR outputs 1 when at least one input is 1. "
            "It models the disjunction of Boolean variables."
        ),
    },
    "NOT": {
        "inputs": 1,
        "fn": lambda a: int(not bool(a)),
        "symbol": "'",
        "expression": "Y = A'",
        "description": (
            "NOT (inverter) flips the input: 0 becomes 1 and 1 becomes 0. "
            "It is the complement operation."
        ),
    },
    "NAND": {
        "inputs": 2,
        "fn": lambda a, b: int(not (bool(a) and bool(b))),
        "symbol": "↑",
        "expression": "Y = (A · B)'",
        "description": (
            "NAND is AND followed by NOT. It outputs 0 only when both inputs are 1. "
            "NAND is functionally complete — any gate can be built from NAND alone."
        ),
    },
    "NOR": {
        "inputs": 2,
        "fn": lambda a, b: int(not (bool(a) or bool(b))),
        "symbol": "↓",
        "expression": "Y = (A + B)'",
        "description": (
            "NOR is OR followed by NOT. It outputs 1 only when every input is 0. "
            "NOR is also functionally complete."
        ),
    },
    "XOR": {
        "inputs": 2,
        "fn": lambda a, b: int(bool(a) != bool(b)),
        "symbol": "⊕",
        "expression": "Y = A ⊕ B",
        "description": (
            "XOR (exclusive OR) outputs 1 when the inputs differ. "
            "Useful for parity, comparison, and arithmetic circuits."
        ),
    },
    "XNOR": {
        "inputs": 2,
        "fn": lambda a, b: int(bool(a) == bool(b)),
        "symbol": "⊙",
        "expression": "Y = A ⊙ B",
        "description": (
            "XNOR (equivalence) outputs 1 when the inputs are the same. "
            "It is XOR followed by NOT."
        ),
    },
}


def available_gates() -> list[str]:
    return list(GATES.keys())


def gate_info(name: str) -> dict:
    key = name.upper()
    if key not in GATES:
        raise ValueError(f"Unknown gate: {name}")
    return GATES[key]


def evaluate_gate(name: str, *inputs: int) -> int:
    """Evaluate a named gate for given 0/1 inputs."""
    info = gate_info(name)
    expected = info["inputs"]
    if len(inputs) != expected:
        raise ValueError(f"{name} expects {expected} input(s), got {len(inputs)}")
    for bit in inputs:
        if bit not in (0, 1):
            raise ValueError(f"Inputs must be 0 or 1, got {bit}")
    return int(info["fn"](*inputs))


def truth_table(name: str) -> list[dict]:
    """Return all input/output rows for a gate as a list of dicts."""
    info = gate_info(name)
    n = info["inputs"]
    rows: list[dict] = []
    for i in range(2**n):
        if n == 1:
            a = (i >> 0) & 1
            y = evaluate_gate(name, a)
            rows.append({"A": a, "Y": y})
        else:
            a = (i >> 1) & 1
            b = (i >> 0) & 1
            y = evaluate_gate(name, a, b)
            rows.append({"A": a, "B": b, "Y": y})
    return rows
