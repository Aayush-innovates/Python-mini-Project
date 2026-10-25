"""Unit tests for logic gates — all input combinations."""

import pytest

from modules.gates import available_gates, evaluate_gate, truth_table


EXPECTED = {
    "AND": {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1},
    "OR": {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1},
    "NOT": {(0,): 1, (1,): 0},
    "NAND": {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0},
    "NOR": {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 0},
    "XOR": {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0},
    "XNOR": {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 1},
}


def test_available_gates():
    gates = available_gates()
    assert set(gates) == set(EXPECTED.keys())


@pytest.mark.parametrize("gate,cases", list(EXPECTED.items()))
def test_all_combinations(gate, cases):
    for inputs, expected in cases.items():
        assert evaluate_gate(gate, *inputs) == expected


def test_truth_table_sizes():
    assert len(truth_table("NOT")) == 2
    assert len(truth_table("AND")) == 4
    assert truth_table("XOR")[-1]["Y"] == 0


def test_invalid_gate():
    with pytest.raises(ValueError):
        evaluate_gate("FOO", 1, 0)


def test_invalid_arity():
    with pytest.raises(ValueError):
        evaluate_gate("AND", 1)


def test_invalid_bit():
    with pytest.raises(ValueError):
        evaluate_gate("OR", 2, 0)
