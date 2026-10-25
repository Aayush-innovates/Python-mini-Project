"""Karnaugh map grouping and SOP simplification for 2–4 variables."""

from __future__ import annotations

from itertools import combinations
from typing import Any

# Gray-code axis labels
GRAY2 = ["00", "01", "11", "10"]
GRAY1 = ["0", "1"]

VAR_NAMES = {
    2: ("A", "B"),
    3: ("A", "B", "C"),
    4: ("A", "B", "C", "D"),
}


def gray_code(n: int) -> list[str]:
    if n == 1:
        return GRAY1.copy()
    if n == 2:
        return GRAY2.copy()
    raise ValueError("Only 1 or 2 bit gray codes needed for K-map axes")


def axis_layout(n_vars: int) -> tuple[list[str], list[str], list[str], list[str]]:
    """
    Return (row_vars, col_vars, row_labels, col_labels).
    Layout:
      2-var: rows A, cols B
      3-var: rows A, cols BC
      4-var: rows AB, cols CD
    """
    if n_vars == 2:
        return ["A"], ["B"], gray_code(1), gray_code(1)
    if n_vars == 3:
        return ["A"], ["B", "C"], gray_code(1), gray_code(2)
    if n_vars == 4:
        return ["A", "B"], ["C", "D"], gray_code(2), gray_code(2)
    raise ValueError("K-Map supports 2, 3, or 4 variables only")


def cell_minterm(row_bits: str, col_bits: str) -> int:
    """Convert concatenated gray-code bits to minterm index."""
    bits = row_bits + col_bits
    return int(bits, 2)


def build_kmap(n_vars: int, minterms: list[int], dont_cares: list[int] | None = None) -> dict[str, Any]:
    """Build K-map grid data."""
    dont_cares = dont_cares or []
    max_m = 2**n_vars
    for m in minterms + dont_cares:
        if m < 0 or m >= max_m:
            raise ValueError(f"Minterm {m} out of range for {n_vars}-variable map (0–{max_m - 1})")

    row_vars, col_vars, row_labels, col_labels = axis_layout(n_vars)
    grid: list[list[str]] = []
    index_grid: list[list[int]] = []
    ones: set[int] = set(minterms)
    xes: set[int] = set(dont_cares)

    for r in row_labels:
        row_vals: list[str] = []
        row_idx: list[int] = []
        for c in col_labels:
            m = cell_minterm(r, c)
            row_idx.append(m)
            if m in ones:
                row_vals.append("1")
            elif m in xes:
                row_vals.append("X")
            else:
                row_vals.append("0")
        grid.append(row_vals)
        index_grid.append(row_idx)

    return {
        "n_vars": n_vars,
        "variables": VAR_NAMES[n_vars],
        "row_vars": row_vars,
        "col_vars": col_vars,
        "row_labels": row_labels,
        "col_labels": col_labels,
        "grid": grid,
        "index_grid": index_grid,
        "minterms": sorted(ones),
        "dont_cares": sorted(xes),
    }


def _bit_count(x: int) -> int:
    return bin(x).count("1")


def _is_power_of_two(x: int) -> bool:
    return x > 0 and (x & (x - 1)) == 0


def _combine(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int] | None:
    """
    Quine–McCluskey style combine.
    Each implicant is (value, mask) where mask bits are dashes (don't care positions).
    """
    va, ma = a
    vb, mb = b
    if ma != mb:
        return None
    diff = va ^ vb
    if _is_power_of_two(diff):
        return (va & ~diff, ma | diff)
    return None


def _covers(implicant: tuple[int, int], minterm: int) -> bool:
    value, mask = implicant
    return (minterm & ~mask) == (value & ~mask)


def _implicant_minterms(implicant: tuple[int, int], n_vars: int) -> list[int]:
    value, mask = implicant
    dash_positions = [i for i in range(n_vars) if mask & (1 << i)]
    results = []
    k = len(dash_positions)
    for bits in range(2**k):
        m = value
        for j, pos in enumerate(dash_positions):
            if bits & (1 << j):
                m |= 1 << pos
            else:
                m &= ~(1 << pos)
        # value already has fixed bits; for dash=0 clear, dash=1 set
        # Rebuild cleanly:
        m = value & ~mask
        for j, pos in enumerate(dash_positions):
            if bits & (1 << j):
                m |= 1 << pos
        results.append(m)
    return sorted(set(results))


def find_prime_implicants(n_vars: int, minterms: list[int], dont_cares: list[int] | None = None) -> list[tuple[int, int]]:
    """Quine–McCluskey prime implicants. Returns list of (value, mask)."""
    dont_cares = dont_cares or []
    onset = sorted(set(minterms) | set(dont_cares))
    if not onset:
        return []

    # Start with single minterms as implicants (value, mask=0)
    current: set[tuple[int, int]] = {(m, 0) for m in onset}
    primes: set[tuple[int, int]] = set()

    while current:
        combined_flags: dict[tuple[int, int], bool] = {imp: False for imp in current}
        next_round: set[tuple[int, int]] = set()
        items = list(current)
        for i, j in combinations(range(len(items)), 2):
            merged = _combine(items[i], items[j])
            if merged is not None:
                next_round.add(merged)
                combined_flags[items[i]] = True
                combined_flags[items[j]] = True
        for imp, used in combined_flags.items():
            if not used:
                primes.add(imp)
        current = next_round

    # Keep only primes that cover at least one true minterm (not only don't-cares)
    true_set = set(minterms)
    return [p for p in primes if any(_covers(p, m) for m in true_set)]


def select_essential_cover(
    n_vars: int, minterms: list[int], primes: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Greedy / essential prime implicant cover."""
    uncovered = set(minterms)
    selected: list[tuple[int, int]] = []
    remaining = list(primes)

    while uncovered:
        # Essential: only one PI covers a minterm
        essentials = []
        for m in list(uncovered):
            covers_m = [p for p in remaining if _covers(p, m)]
            if len(covers_m) == 1:
                if covers_m[0] not in essentials:
                    essentials.append(covers_m[0])
        if essentials:
            for e in essentials:
                if e in remaining:
                    selected.append(e)
                    remaining.remove(e)
                    uncovered -= {m for m in uncovered if _covers(e, m)}
            continue
        # Otherwise pick PI covering most uncovered minterms
        if not remaining:
            break
        best = max(remaining, key=lambda p: sum(1 for m in uncovered if _covers(p, m)))
        selected.append(best)
        remaining.remove(best)
        uncovered -= {m for m in uncovered if _covers(best, m)}

    return selected


def implicant_to_term(implicant: tuple[int, int], n_vars: int) -> str:
    """Convert (value, mask) to a product term like A·B'·C."""
    names = VAR_NAMES[n_vars]
    value, mask = implicant
    literals = []
    # Bit significance: bit (n_vars-1) = first variable
    for i, name in enumerate(names):
        bit_pos = n_vars - 1 - i
        if mask & (1 << bit_pos):
            continue  # dash — variable eliminated
        if value & (1 << bit_pos):
            literals.append(name)
        else:
            literals.append(f"{name}'")
    if not literals:
        return "1"
    return "*".join(literals)


def group_cells(n_vars: int, implicant: tuple[int, int]) -> list[int]:
    """Minterms covered by an implicant (for visualization)."""
    return _implicant_minterms(implicant, n_vars)


def solve_kmap(
    n_vars: int, minterms: list[int], dont_cares: list[int] | None = None
) -> dict[str, Any]:
    """
    Full K-map solve: grid, groups, and simplified SOP.
    """
    dont_cares = dont_cares or []
    kmap = build_kmap(n_vars, minterms, dont_cares)

    if not minterms:
        return {
            **kmap,
            "groups": [],
            "sop": "0",
            "prime_implicants": [],
        }

    primes = find_prime_implicants(n_vars, minterms, dont_cares)
    cover = select_essential_cover(n_vars, minterms, primes)

    groups = []
    terms = []
    for imp in cover:
        cells = group_cells(n_vars, imp)
        term = implicant_to_term(imp, n_vars)
        groups.append({"implicant": imp, "minterms": cells, "term": term})
        terms.append(term)

    # Sort terms for stable output
    terms = sorted(set(terms), key=lambda t: (len(t), t))
    sop = " + ".join(terms) if terms else "0"

    return {
        **kmap,
        "groups": groups,
        "sop": sop,
        "prime_implicants": primes,
    }
