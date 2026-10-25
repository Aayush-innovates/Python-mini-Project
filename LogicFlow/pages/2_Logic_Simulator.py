"""Logic Gate Simulator page."""

import streamlit as st

from components.ui import apply_theme, bit_badge, page_header, sidebar_brand
from components.visualizations import render_gate_diagram, show_truth_table
from modules.gates import available_gates, evaluate_gate, gate_info, truth_table

st.set_page_config(page_title="Logic Simulator · LogicFlow", page_icon="🔌", layout="wide")
apply_theme()
sidebar_brand()
page_header("Logic Gate Simulator", "Interactive demonstration of fundamental digital logic gates.")

gate = st.selectbox("Select gate", available_gates(), index=0)
info = gate_info(gate)

st.markdown(f"**Boolean expression:** `{info['expression']}`")
st.write(info["description"])

col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.subheader("Inputs")
    if info["inputs"] == 1:
        a = st.radio("Input A", [0, 1], horizontal=True, key=f"{gate}_a")
        inputs = [int(a)]
    else:
        a = st.radio("Input A", [0, 1], horizontal=True, key=f"{gate}_a")
        b = st.radio("Input B", [0, 1], horizontal=True, key=f"{gate}_b")
        inputs = [int(a), int(b)]

    output = evaluate_gate(gate, *inputs)
    st.markdown("**Output Y**")
    st.markdown(bit_badge(output), unsafe_allow_html=True)

with col_out:
    st.subheader("Gate diagram")
    render_gate_diagram(gate, inputs, output)

st.subheader("Complete truth table")
show_truth_table(truth_table(gate))
