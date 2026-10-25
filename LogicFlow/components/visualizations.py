"""Visualizations: gate diagrams, K-maps, and SOP circuit schematics.

Uses st.components.v1.html so SVG is not stripped by Streamlit markdown sanitizer.
"""

from __future__ import annotations

import html as html_lib
import re
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

NAVY = "#0A2540"
ACCENT = "#1B4F72"
ONE_BG = "#D8F3E3"
ONE_FG = "#0E5C36"
ZERO_BG = "#EEF2F6"
ZERO_FG = "#475569"
X_BG = "#FFF3CD"
X_FG = "#7A5B00"
GROUP_COLORS = [
    "#1B7F4E",
    "#1B4F72",
    "#B47814",
    "#8C2850",
    "#3C64B4",
    "#643CA0",
]


def _show_html(content: str, height: int = 220):
    """Render raw HTML/SVG reliably inside Streamlit."""
    components.html(
        f"""
        <div style="font-family:'Segoe UI',Arial,sans-serif;">
        {content}
        </div>
        """,
        height=height,
        scrolling=True,
    )


def show_truth_table(rows: list[dict]):
    if not rows:
        st.info("No rows to display.")
        return
    st.dataframe(rows, width="stretch", hide_index=True)


# ---------------------------------------------------------------------------
# Single logic-gate schematics (Logic Simulator)
# ---------------------------------------------------------------------------

def _gate_body_svg(gate: str, x: float, y: float, w: float, h: float) -> str:
    """Draw classic gate body; returns SVG snippet. Output tip at right mid."""
    stroke = NAVY
    fill = "rgba(27,79,114,0.12)"
    cx = x + w * 0.55
    cy = y + h / 2
    bubble = ""

    if gate in ("AND", "NAND"):
        # Rectangle + semicircle
        body = f"""
        <path d="M {x} {y} L {x + w * 0.45} {y}
                 A {w * 0.45} {h / 2} 0 0 1 {x + w * 0.45} {y + h}
                 L {x} {y + h} Z"
              fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>
        """
        tip_x = x + w * 0.9
        if gate == "NAND":
            bubble = f'<circle cx="{tip_x}" cy="{cy}" r="7" fill="#fff" stroke="{stroke}" stroke-width="2.5"/>'
            tip_x += 7
    elif gate in ("OR", "NOR", "XOR", "XNOR"):
        # OR-like curved shape
        body = f"""
        <path d="M {x} {y}
                 Q {x + w * 0.35} {cy} {x} {y + h}
                 Q {x + w * 0.55} {y + h} {x + w * 0.95} {cy}
                 Q {x + w * 0.55} {y} {x} {y} Z"
              fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>
        """
        tip_x = x + w * 0.95
        if gate in ("XOR", "XNOR"):
            body = f"""
            <path d="M {x - 10} {y} Q {x + w * 0.2} {cy} {x - 10} {y + h}"
                  fill="none" stroke="{stroke}" stroke-width="2.5"/>
            """ + body
        if gate in ("NOR", "XNOR"):
            bubble = f'<circle cx="{tip_x}" cy="{cy}" r="7" fill="#fff" stroke="{stroke}" stroke-width="2.5"/>'
            tip_x += 7
    else:  # NOT
        body = f"""
        <path d="M {x} {y} L {x + w * 0.85} {cy} L {x} {y + h} Z"
              fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>
        """
        tip_x = x + w * 0.85
        bubble = f'<circle cx="{tip_x + 7}" cy="{cy}" r="7" fill="#fff" stroke="{stroke}" stroke-width="2.5"/>'
        tip_x += 14

    label = f"""
    <text x="{cx}" y="{cy + 5}" text-anchor="middle" fill="{NAVY}"
          font-size="13" font-weight="700">{gate}</text>
    """
    return body + bubble + label, tip_x, cy


def render_gate_diagram(gate_name: str, inputs: list[int], output: int):
    """Classic single-gate schematic with live 0/1 values."""
    gate = gate_name.upper()
    out_color = ONE_FG if output == 1 else "#94A3B8"

    if len(inputs) == 1:
        wires = f"""
        <line x1="30" y1="90" x2="120" y2="90" stroke="{NAVY}" stroke-width="3"/>
        <circle cx="30" cy="90" r="6" fill="{ONE_FG if inputs[0] else '#94A3B8'}"/>
        <text x="8" y="75" fill="{NAVY}" font-size="14" font-weight="600">A={inputs[0]}</text>
        """
        body, tip_x, tip_y = _gate_body_svg(gate, 120, 40, 130, 100)
    else:
        wires = f"""
        <line x1="30" y1="55" x2="120" y2="55" stroke="{NAVY}" stroke-width="3"/>
        <line x1="30" y1="125" x2="120" y2="125" stroke="{NAVY}" stroke-width="3"/>
        <circle cx="30" cy="55" r="6" fill="{ONE_FG if inputs[0] else '#94A3B8'}"/>
        <circle cx="30" cy="125" r="6" fill="{ONE_FG if inputs[1] else '#94A3B8'}"/>
        <text x="8" y="42" fill="{NAVY}" font-size="14" font-weight="600">A={inputs[0]}</text>
        <text x="8" y="148" fill="{NAVY}" font-size="14" font-weight="600">B={inputs[1]}</text>
        """
        body, tip_x, tip_y = _gate_body_svg(gate, 120, 40, 130, 100)

    svg = f"""
    <div style="background:#fff;border:1px solid #D0D7DE;border-radius:10px;padding:8px 12px;">
      <div style="color:{NAVY};font-weight:700;margin-bottom:4px;">{gate} Gate Schematic</div>
      <svg viewBox="0 0 400 180" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">
        {wires}
        {body}
        <line x1="{tip_x}" y1="{tip_y}" x2="340" y2="{tip_y}" stroke="{NAVY}" stroke-width="3"/>
        <circle cx="350" cy="{tip_y}" r="9" fill="{out_color}"/>
        <text x="365" y="{tip_y + 5}" fill="{NAVY}" font-size="15" font-weight="700">Y={output}</text>
      </svg>
    </div>
    """
    _show_html(svg, height=240)


# ---------------------------------------------------------------------------
# SOP parsing + multi-gate circuit diagram
# ---------------------------------------------------------------------------

def format_minimized_equation(sop: Any) -> str:
    """Human-readable minimized Boolean equation Y = ..."""
    s = str(sop).strip()
    if s in ("0", "False", "false"):
        return "Y = 0"
    if s in ("1", "True", "true"):
        return "Y = 1"

    # SymPy style → textbook style
    s = s.replace("True", "1").replace("False", "0")
    s = re.sub(r"\bNot\(([^)]+)\)", r"\1'", s)
    s = s.replace("~", "")
    # After removing ~, need to put ' on next token — handle ~A already as A' via:
    # redo more carefully
    s = str(sop).strip()
    s = s.replace("True", "1").replace("False", "0")
    s = re.sub(r"~([A-Za-z0-9]+)", r"\1'", s)
    s = re.sub(r"Not\(([A-Za-z0-9]+)\)", r"\1'", s)
    s = s.replace("&", "*").replace("|", " + ")
    s = s.replace("∧", "*").replace("∨", " + ")
    s = re.sub(r"\s+", " ", s).strip()
    # Remove redundant outer parens around whole expr
    if s.startswith("(") and s.endswith(")") and s.count("(") == 1:
        s = s[1:-1]
    return f"Y = {s}"


def parse_sop_terms(sop: Any) -> list[list[tuple[str, bool]]]:
    """
    Parse SOP into product terms.
    Each term = list of (variable, is_true) where is_true=False means complemented.
    """
    s = str(sop).strip()
    if s in ("0", "False", "false"):
        return []
    if s in ("1", "True", "true"):
        return [[]]  # constant 1 — empty product

    # Normalize to + separated, * within terms, ' for complement
    s = s.replace("True", "1").replace("False", "0")
    s = re.sub(r"~([A-Za-z0-9]+)", r"\1'", s)
    s = re.sub(r"Not\(([A-Za-z0-9]+)\)", r"\1'", s)
    s = s.replace("|", "+").replace("&", "*")
    s = s.replace("∨", "+").replace("∧", "*")
    s = s.replace("·", "*")
    s = re.sub(r"[()]", "", s)

    terms_out: list[list[tuple[str, bool]]] = []
    for raw_term in s.split("+"):
        term = raw_term.strip()
        if not term:
            continue
        if term == "1":
            terms_out.append([])
            continue
        if term == "0":
            continue
        literals: list[tuple[str, bool]] = []
        # tokens like A, A', B, B' separated by * or juxtaposition
        parts = re.findall(r"[A-Za-z][A-Za-z0-9]*'?", term.replace("*", " "))
        if not parts:
            # try split by *
            parts = [p for p in term.split("*") if p.strip()]
        for p in parts:
            p = p.strip()
            if not p:
                continue
            if p.endswith("'"):
                literals.append((p[:-1], False))
            else:
                literals.append((p, True))
        if literals:
            terms_out.append(literals)
    return terms_out


def render_sop_circuit(sop: Any, title: str = "Gate-level realization"):
    """
    Draw a two-level AND-OR (SOP) circuit for the minimized expression.
    Complemented literals use an inverter bubble on the AND input.
    """
    equation = format_minimized_equation(sop)
    terms = parse_sop_terms(sop)
    header = f"""
    <div style="background:#fff;border:1px solid #D0D7DE;border-radius:10px;padding:12px;">
      <div style="color:{NAVY};font-weight:700;margin-bottom:4px;">{html_lib.escape(title)}</div>
      <div style="margin:6px 0 10px 0;font-size:1.25rem;color:{ACCENT};font-weight:700;">
        {html_lib.escape(equation)}
      </div>
    """

    if str(sop).strip() in ("0", "False", "false"):
        _show_html(
            header
            + f'<p style="color:{NAVY};">Constant <b>0</b> — output tied to logic 0.</p></div>',
            height=120,
        )
        return

    if len(terms) == 1 and terms[0] == []:
        _show_html(
            header
            + f'<p style="color:{NAVY};">Constant <b>1</b> — output tied to logic 1.</p></div>',
            height=120,
        )
        return

    if not terms:
        _show_html(header + f'<p style="color:{NAVY};">No product terms.</p></div>', height=120)
        return

    n_terms = len(terms)
    row_h = 78
    top = 20
    height = top + n_terms * row_h + 30
    width = 540
    and_x, and_w = 190, 72
    bus_x = 300
    or_x = 330

    parts = [
        header,
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{min(height + 10, 480)}" '
        f'xmlns="http://www.w3.org/2000/svg">',
    ]
    and_outs: list[tuple[float, float]] = []

    for ti, term in enumerate(terms):
        cy = top + ti * row_h + row_h / 2

        # Single literal: no AND needed — wire (with optional bubble) toward OR/Y
        if len(term) == 1:
            var, is_true = term[0]
            label = var if is_true else f"{var}'"
            parts.append(
                f'<text x="16" y="{cy + 4}" fill="{NAVY}" font-size="13" font-weight="600">{label}</text>'
                f'<line x1="55" y1="{cy}" x2="{bus_x}" y2="{cy}" stroke="{NAVY}" stroke-width="2"/>'
            )
            if not is_true:
                parts.append(
                    f'<circle cx="70" cy="{cy}" r="5" fill="#fff" stroke="{NAVY}" stroke-width="2"/>'
                )
            and_outs.append((bus_x, cy))
            continue

        lit_count = len(term)
        and_h = max(40, 18 * lit_count + 10)
        and_y = cy - and_h / 2

        for li, (var, is_true) in enumerate(term):
            ly = and_y + (li + 0.5) * (and_h / lit_count)
            label = var if is_true else f"{var}'"
            parts.append(
                f'<text x="16" y="{ly + 4}" fill="{NAVY}" font-size="13" font-weight="600">{label}</text>'
                f'<line x1="55" y1="{ly}" x2="{and_x}" y2="{ly}" stroke="{NAVY}" stroke-width="2"/>'
            )
            if not is_true:
                parts.append(
                    f'<circle cx="{and_x - 6}" cy="{ly}" r="5" fill="#fff" stroke="{NAVY}" stroke-width="2"/>'
                )

        gate_label = "AND" if lit_count > 1 else ""
        parts.append(
            f'<rect x="{and_x}" y="{and_y}" width="{and_w}" height="{and_h}" rx="8" '
            f'fill="rgba(27,79,114,0.12)" stroke="{NAVY}" stroke-width="2"/>'
            f'<text x="{and_x + and_w / 2}" y="{cy + 4}" text-anchor="middle" '
            f'fill="{NAVY}" font-size="12" font-weight="700">{gate_label}</text>'
            f'<line x1="{and_x + and_w}" y1="{cy}" x2="{bus_x}" y2="{cy}" '
            f'stroke="{NAVY}" stroke-width="2"/>'
        )
        and_outs.append((bus_x, cy))

    # Output stage
    if n_terms == 1:
        _, cy = and_outs[0]
        parts.append(
            f'<line x1="{bus_x}" y1="{cy}" x2="470" y2="{cy}" stroke="{NAVY}" stroke-width="2.5"/>'
            f'<circle cx="480" cy="{cy}" r="8" fill="{ONE_FG}"/>'
            f'<text x="495" y="{cy + 5}" fill="{NAVY}" font-size="14" font-weight="700">Y</text>'
        )
    else:
        or_h = max(56, n_terms * 30)
        or_cy = top + (n_terms * row_h) / 2
        or_y = or_cy - or_h / 2
        for i, (px, py) in enumerate(and_outs):
            ty = or_y + (i + 0.5) * (or_h / n_terms)
            parts.append(
                f'<line x1="{px}" y1="{py}" x2="{or_x}" y2="{ty}" stroke="{NAVY}" stroke-width="2"/>'
            )
        parts.append(
            f'<path d="M {or_x} {or_y} Q {or_x + 28} {or_cy} {or_x} {or_y + or_h} '
            f'Q {or_x + 48} {or_y + or_h} {or_x + 78} {or_cy} '
            f'Q {or_x + 48} {or_y} {or_x} {or_y} Z" '
            f'fill="rgba(27,127,78,0.12)" stroke="{NAVY}" stroke-width="2.5"/>'
            f'<text x="{or_x + 36}" y="{or_cy + 4}" text-anchor="middle" '
            f'fill="{NAVY}" font-size="12" font-weight="700">OR</text>'
            f'<line x1="{or_x + 78}" y1="{or_cy}" x2="470" y2="{or_cy}" '
            f'stroke="{NAVY}" stroke-width="2.5"/>'
            f'<circle cx="480" cy="{or_cy}" r="8" fill="{ONE_FG}"/>'
            f'<text x="495" y="{or_cy + 5}" fill="{NAVY}" font-size="14" font-weight="700">Y</text>'
        )

    parts.append("</svg></div>")
    _show_html("".join(parts), height=min(height + 110, 560))


def render_kmap(kmap: dict[str, Any], groups: list[dict] | None = None):
    """HTML Karnaugh map with group highlights."""
    groups = groups or []
    grid = kmap["grid"]
    index_grid = kmap["index_grid"]
    row_labels = kmap["row_labels"]
    col_labels = kmap["col_labels"]
    row_vars = "".join(kmap["row_vars"])
    col_vars = "".join(kmap["col_vars"])

    membership: dict[int, list[int]] = {}
    for gi, g in enumerate(groups):
        for m in g["minterms"]:
            membership.setdefault(m, []).append(gi)

    header_cells = "".join(
        f'<th style="padding:10px;background:{NAVY};color:#fff;border:1px solid #fff;">{lab}</th>'
        for lab in col_labels
    )

    body_rows = []
    for r, rlab in enumerate(row_labels):
        cells = []
        for c, _ in enumerate(col_labels):
            val = grid[r][c]
            m = index_grid[r][c]
            if val == "1":
                bg, fg = ONE_BG, ONE_FG
            elif val == "X":
                bg, fg = X_BG, X_FG
            else:
                bg, fg = ZERO_BG, ZERO_FG

            borders = ""
            for gi in membership.get(m, []):
                color = GROUP_COLORS[gi % len(GROUP_COLORS)]
                borders += f"inset 0 0 0 3px {color},"
            box_shadow = borders.rstrip(",") if borders else "none"

            cells.append(
                f"""<td style="padding:14px 10px;text-align:center;background:{bg};
                color:{fg};border:1px solid #CBD5E1;font-weight:700;box-shadow:{box_shadow};">
                <div style="font-size:1.25rem;">{val}</div>
                <div style="font-size:0.75rem;font-weight:500;opacity:0.8;">m{m}</div>
                </td>"""
            )
        body_rows.append(
            f'<tr><th style="padding:10px;background:{ACCENT};color:#fff;border:1px solid #fff;">{rlab}</th>'
            + "".join(cells)
            + "</tr>"
        )

    legend = ""
    if groups:
        chips = []
        for i, g in enumerate(groups):
            color = GROUP_COLORS[i % len(GROUP_COLORS)]
            chips.append(
                f'<span style="display:inline-block;margin:4px 8px 4px 0;padding:4px 10px;'
                f'border:2px solid {color};border-radius:6px;color:{NAVY};font-size:0.9rem;">'
                f'G{i + 1}: {html_lib.escape(g["term"])} '
                f'{{{", ".join(str(x) for x in g["minterms"])}}}</span>'
            )
        legend = "<div style='margin-top:12px;'>" + "".join(chips) + "</div>"

    n_rows = len(row_labels)
    html = f"""
    <div style="background:#fff;border:1px solid #D0D7DE;border-radius:10px;padding:16px;overflow-x:auto;">
      <div style="color:{NAVY};font-weight:700;margin-bottom:10px;">
        {kmap['n_vars']}-Variable Karnaugh Map
        <span style="font-weight:500;color:#64748B;"> · rows: {row_vars} · cols: {col_vars}</span>
      </div>
      <table style="border-collapse:collapse;margin:0 auto;">
        <thead>
          <tr>
            <th style="padding:10px;background:{NAVY};color:#fff;border:1px solid #fff;">{row_vars}\\{col_vars}</th>
            {header_cells}
          </tr>
        </thead>
        <tbody>
          {''.join(body_rows)}
        </tbody>
      </table>
      {legend}
    </div>
    """
    _show_html(html, height=180 + n_rows * 70 + (60 if groups else 0))
