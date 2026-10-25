"""Karnaugh Map Solver page."""

import streamlit as st

from components.ui import apply_theme, page_header, sidebar_brand
from components.visualizations import format_minimized_equation, render_kmap, render_sop_circuit
from modules.kmap_solver import VAR_NAMES, solve_kmap

st.set_page_config(page_title="K-Map Solver · LogicFlow", page_icon="▦", layout="wide")
apply_theme()
sidebar_brand()
page_header(
    "Karnaugh Map Solver",
    "Select minterms → grouped K-map → minimized SOP equation + gate circuit.",
)

n_vars = st.selectbox("Number of variables", [2, 3, 4], index=1)
max_m = 2**n_vars - 1
var_names = ", ".join(VAR_NAMES[n_vars])
st.caption(f"Variables: **{var_names}** · Valid minterms: **0 – {max_m}**")

defaults = {2: [0, 1, 2], 3: [0, 1, 2, 5], 4: [0, 1, 2, 3, 5, 7]}
minterm_options = list(range(max_m + 1))

minterms = st.multiselect(
    "Select minterms (place 1 in these cells)",
    options=minterm_options,
    default=[m for m in defaults[n_vars] if m <= max_m],
    key=f"minterms_{n_vars}",
)
dont_cares = st.multiselect(
    "Don't-cares (optional)",
    options=[m for m in minterm_options if m not in minterms],
    default=[],
    key=f"dc_{n_vars}",
)

overlap = set(minterms) & set(dont_cares)
if overlap:
    st.error(f"Minterms and don't-cares cannot overlap: {sorted(overlap)}")
else:
    try:
        result = solve_kmap(n_vars, list(minterms), list(dont_cares))
        minimized = format_minimized_equation(result["sop"])

        st.subheader("Karnaugh map")
        render_kmap(result, result["groups"])

        st.subheader("Final minimized equation")
        st.markdown(
            f"<div style='font-size:1.6rem;font-weight:700;color:#0A2540;"
            f"background:#fff;border:1px solid #D0D7DE;border-radius:10px;"
            f"padding:14px 18px;margin-bottom:12px;'>{minimized}</div>",
            unsafe_allow_html=True,
        )

        st.subheader("Gate representation (SOP)")
        render_sop_circuit(result["sop"], title="K-Map SOP → AND-OR circuit")

        if result["groups"]:
            with st.expander("Groups formed", expanded=True):
                for i, g in enumerate(result["groups"], start=1):
                    st.markdown(
                        f"**Group {i}:** minterms `{g['minterms']}` → `{g['term']}`"
                    )
        else:
            st.info("No 1-cells selected — the function simplifies to **0**.")
    except ValueError as exc:
        st.error(str(exc))
