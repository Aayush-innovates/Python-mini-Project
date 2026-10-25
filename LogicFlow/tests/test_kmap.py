"""Unit tests for Karnaugh map solver."""

import pytest

from modules.kmap_solver import build_kmap, cell_minterm, solve_kmap


def test_cell_minterm_gray():
    # 2-var: row A, col B
    assert cell_minterm("0", "0") == 0
    assert cell_minterm("0", "1") == 1
    assert cell_minterm("1", "0") == 2
    assert cell_minterm("1", "1") == 3


def test_build_kmap_2var():
    km = build_kmap(2, [1, 3])
    assert km["n_vars"] == 2
    flat = [v for row in km["grid"] for v in row]
    assert flat.count("1") == 2


def test_solve_all_ones_2var():
    result = solve_kmap(2, [0, 1, 2, 3])
    assert result["sop"] == "1"


def test_solve_single_minterm():
    result = solve_kmap(2, [3])
    assert "A" in result["sop"] and "B" in result["sop"]
    assert "'" not in result["sop"].replace(" ", "")


def test_solve_3var_known():
    # F = Σ(0,1,2,5) — common teaching example; SOP should be compact
    result = solve_kmap(3, [0, 1, 2, 5])
    assert result["sop"] != "0"
    assert len(result["groups"]) >= 1
    # Cover all minterms
    covered = set()
    for g in result["groups"]:
        covered.update(g["minterms"])
    assert set([0, 1, 2, 5]).issubset(covered)


def test_solve_4var():
    result = solve_kmap(4, [0, 1, 2, 3])
    assert result["sop"] != "0"
    covered = set()
    for g in result["groups"]:
        covered.update(m for m in g["minterms"] if m in {0, 1, 2, 3})
    assert covered == {0, 1, 2, 3}


def test_empty_minterms():
    result = solve_kmap(3, [])
    assert result["sop"] == "0"


def test_out_of_range():
    with pytest.raises(ValueError):
        build_kmap(2, [5])
