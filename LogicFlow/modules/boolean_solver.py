"""Boolean expression parsing, truth tables, and simplification via SymPy."""

from __future__ import annotations

import re
from typing import Any

import sympy
from sympy.logic.boolalg import SOPform, simplify_logic, to_dnf
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

_ALLOWED = re.compile(r"^[A-Za-z0-9\s\+\*\·\&\|\^\~\!\'\(\)]+$")


def normalize_expression(expr: str) -> str:
    """
    Convert common Boolean notation into SymPy-friendly Python syntax.

    Supported: A+B, A*B, A·B, A&B, A|B, A^B, A', ~A, !A, (A+B)'
    """
    if expr is None:
        raise ValueError("Expression is empty.")
    s = expr.strip()
    if not s:
        raise ValueError("Expression is empty.")
    if not _ALLOWED.match(s):
        raise ValueError(
            "Invalid characters. Use letters, +, *, ·, &, |, ^, ~, !, ', and parentheses."
        )

    # Postfix complement: (expr)' or A'
    while True:
        m = re.search(r"(\([^()]*\))'", s)
        if m:
            s = s[: m.start()] + "~(" + m.group(1) + ")" + s[m.end() :]
            continue
        m = re.search(r"([A-Za-z0-9])'", s)
        if m:
            s = s[: m.start()] + "~" + m.group(1) + s[m.end() :]
            continue
        break

    s = s.replace("·", "*")
    s = s.replace("!", "~")

    # XOR before OR mapping: A^B -> Xor(A,B)
    prev = None
    while prev != s:
        prev = s
        s = re.sub(
            r"([A-Za-z0-9\)])\s*\^\s*([A-Za-z0-9\(~])",
            r"Xor(\1,\2)",
            s,
        )

    s = re.sub(r"\+", "|", s)
    s = s.replace("*", "&")
    return s


def parse_boolean(expr: str) -> sympy.Expr:
    """Parse a Boolean expression string into a SymPy Boolean expression."""
    normalized = normalize_expression(expr)
    local_dict = {
        "Xor": sympy.Xor,
        "And": sympy.And,
        "Or": sympy.Or,
        "Not": sympy.Not,
        "true": sympy.true,
        "false": sympy.false,
    }
    transformations = standard_transformations + (implicit_multiplication_application,)
    try:
        parsed = parse_expr(
            normalized,
            local_dict=local_dict,
            transformations=transformations,
            evaluate=False,
        )
    except Exception as exc:
        raise ValueError(
            f"Could not parse expression: {expr!r}. Check operators and parentheses."
        ) from exc

    symbols = sorted(parsed.free_symbols, key=lambda s: s.name)
    bool_map = {s: sympy.symbols(s.name, boolean=True) for s in symbols}
    return parsed.xreplace(bool_map)


def get_variables(expr: sympy.Expr) -> list[sympy.Symbol]:
    return sorted(expr.free_symbols, key=lambda s: s.name)


def _to_bit(result) -> int:
    result = simplify_logic(result)
    if result in (sympy.true, True, 1):
        return 1
    if result in (sympy.false, False, 0):
        return 0
    return int(bool(result))


def truth_table(expr_str: str) -> tuple[list[str], list[dict[str, int]]]:
    """Build a truth table. Returns (variable_names, rows)."""
    expr = parse_boolean(expr_str)
    variables = get_variables(expr)
    names = [v.name for v in variables]
    rows: list[dict[str, int]] = []
    n = len(variables)

    if n == 0:
        return names, [{"Y": _to_bit(expr)}]

    for i in range(2**n):
        assignment = {}
        row: dict[str, int] = {}
        for bit_idx, var in enumerate(variables):
            val = (i >> (n - 1 - bit_idx)) & 1
            assignment[var] = bool(val)
            row[var.name] = val
        row["Y"] = _to_bit(expr.subs(assignment))
        rows.append(row)
    return names, rows


def simplify_expression(expr_str: str) -> dict[str, Any]:
    """Simplify a Boolean expression; steps are taken only from SymPy outputs."""
    expr = parse_boolean(expr_str)
    variables = get_variables(expr)
    simplified = simplify_logic(expr, form="dnf")
    sop = to_dnf(expr, simplify=True)

    steps: list[str] = [
        f"Parsed expression: {expr}",
        f"Variables: {', '.join(v.name for v in variables) or '(none)'}",
        f"SymPy simplify_logic (DNF): {simplified}",
        f"Sum-of-Products (SOP) form: {sop}",
    ]

    if variables:
        _, rows = truth_table(expr_str)
        minterms = [i for i, row in enumerate(rows) if row["Y"] == 1]
        if minterms:
            sop_from_tt = SOPform(variables, minterms)
            steps.append(
                f"SOP reconstructed from truth-table minterms {minterms}: {sop_from_tt}"
            )
            sop = sop_from_tt
            simplified = simplify_logic(sop_from_tt, form="dnf")
        else:
            sop = sympy.false
            simplified = sympy.false
            steps.append("No minterms where Y=1 → function is 0.")

    return {
        "original": expr_str.strip(),
        "sympy_expr": expr,
        "simplified": simplified,
        "sop": sop,
        "variables": variables,
        "steps": steps,
    }


def expressions_equivalent(a: str, b: str) -> bool:
    """Return True if two expressions are logically equivalent."""
    ea = parse_boolean(a)
    eb = parse_boolean(b)
    diff = simplify_logic(sympy.Xor(ea, eb))
    return diff == sympy.false
