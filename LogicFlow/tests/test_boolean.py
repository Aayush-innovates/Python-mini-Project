"""Unit tests for Boolean parsing and equivalence."""

import pytest

from modules.boolean_solver import (
    expressions_equivalent,
    normalize_expression,
    parse_boolean,
    simplify_expression,
    truth_table,
)


def test_normalize_and_or_not():
    assert "&" in normalize_expression("A*B") or "And" in normalize_expression("A*B")
    n = normalize_expression("A'")
    assert "~" in n


def test_parse_simple():
    expr = parse_boolean("A+B")
    assert expr is not None


def test_truth_table_and():
    names, rows = truth_table("A*B")
    assert names == ["A", "B"]
    assert len(rows) == 4
    assert rows[-1]["Y"] == 1
    assert rows[0]["Y"] == 0


def test_simplify_absorption():
    result = simplify_expression("A + A*B")
    # Equivalent to A
    assert expressions_equivalent(str(result["simplified"]), "A")


def test_equivalence_demorgan():
    assert expressions_equivalent("(A*B)'", "A'+B'")
    assert not expressions_equivalent("A+B", "A*B")


def test_sop_present():
    result = simplify_expression("A*B + A*B'")
    assert result["sop"] is not None
    assert expressions_equivalent(str(result["sop"]), "A")


def test_invalid_expression():
    with pytest.raises(ValueError):
        parse_boolean("A + ")


def test_empty_expression():
    with pytest.raises(ValueError):
        parse_boolean("")
