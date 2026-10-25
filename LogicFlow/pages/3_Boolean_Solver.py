"""Boolean Expression Solver page."""

import streamlit as st

from components.ui import apply_theme, page_header, sidebar_brand
from components.visualizations import (
    format_minimized_equation,
    render_sop_circuit,
    show_truth_table,
)
from modules.boolean_solver import simplify_expression, truth_table

st.set_page_config(page_title="Boolean Solver · LogicFlow", page_icon="∑", layout="wide")
apply_theme()
sidebar_brand()
page_header(
    "Boolean Expression Solver",
    "Parse, simplify to a minimized equation, and view the gate-level SOP circuit.",
)

with st.expander("Supported notation", expanded=False):
    st.markdown(
        """
- **OR:** `+` or `|` · **AND:** `*` , `·` , or `&` · **NOT:** `'` / `~` / `!` · **XOR:** `^`
- Examples: `(A+B)*C'` · `A&~B|C` · `A*B + A*B'`
"""
    )

expr = st.text_input("Enter Boolean expression", value="(A+B)*C'")
examples = st.selectbox(
    "Or pick an example",
    [
        "(custom above)",
        "A+A*B",
        "(A*B)'",
        "A*B + A*B'",
        "A^B",
        "(A+B)*(A+C)",
    ],
)
if examples != "(custom above)":
    expr = examples

if st.button("Solve expression", type="primary") or expr:
    try:
        result = simplify_expression(expr)
        names, rows = truth_table(expr)
        minimized = format_minimized_equation(result["sop"])

        st.subheader("Final minimized equation")
        st.markdown(
            f"<div style='font-size:1.6rem;font-weight:700;color:#0A2540;"
            f"background:#fff;border:1px solid #D0D7DE;border-radius:10px;"
            f"padding:14px 18px;margin-bottom:12px;'>{minimized}</div>",
            unsafe_allow_html=True,
        )

        st.subheader("Gate representation (SOP)")
        render_sop_circuit(result["sop"], title="Minimized SOP → AND-OR circuit")

        with st.expander("Details: original / SymPy forms / truth table", expanded=False):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**Original**")
                st.code(result["original"], language="text")
            with c2:
                st.markdown("**Simplified (SymPy)**")
                st.code(str(result["simplified"]), language="text")
            with c3:
                st.markdown("**SOP (SymPy)**")
                st.code(str(result["sop"]), language="text")

            st.markdown("**SymPy-derived notes**")
            for step in result["steps"]:
                st.markdown(f"- {step}")

            st.markdown("**Truth table**")
            show_truth_table(rows)
    except ValueError as exc:
        st.error(str(exc))
