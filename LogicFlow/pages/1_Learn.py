"""Learn DSD — supporting theory module."""

import streamlit as st

from components.ui import apply_theme, info_card, page_header, sidebar_brand

st.set_page_config(page_title="Learn DSD · LogicFlow", page_icon="📘", layout="wide")
apply_theme()
sidebar_brand()
page_header("Learn DSD", "Core Digital System Design concepts for quick revision.")

topic = st.selectbox(
    "Choose a topic",
    [
        "Logic Gates",
        "Boolean Laws",
        "SOP and POS",
        "Minterms and Maxterms",
        "K-Map Fundamentals",
    ],
)

if topic == "Logic Gates":
    info_card(
        "What is a logic gate?",
        "A logic gate is an electronic circuit that implements a Boolean function. "
        "Inputs and outputs are binary (0 or 1). Fundamental gates: AND, OR, NOT. "
        "Derived gates: NAND, NOR, XOR, XNOR.",
    )
    st.markdown(
        """
| Gate | Expression | Behavior |
|------|------------|----------|
| AND | Y = A·B | 1 only if all inputs are 1 |
| OR | Y = A+B | 1 if any input is 1 |
| NOT | Y = A' | Complement of input |
| NAND | Y = (A·B)' | Opposite of AND |
| NOR | Y = (A+B)' | Opposite of OR |
| XOR | Y = A⊕B | 1 if inputs differ |
| XNOR | Y = A⊙B | 1 if inputs match |
"""
    )
    st.info("Open **Logic Simulator** in the sidebar to toggle inputs live.")

elif topic == "Boolean Laws":
    info_card(
        "Boolean algebra",
        "Boolean algebra manipulates binary variables using OR (+), AND (·), and NOT ('). "
        "These identities simplify logic before hardware implementation.",
    )
    st.markdown(
        """
- **Identity:** A + 0 = A ,  A · 1 = A
- **Null / Dominance:** A + 1 = 1 ,  A · 0 = 0
- **Idempotent:** A + A = A ,  A · A = A
- **Complement:** A + A' = 1 ,  A · A' = 0
- **Commutative:** A + B = B + A ,  A · B = B · A
- **Associative:** (A + B) + C = A + (B + C)
- **Distributive:** A · (B + C) = A·B + A·C
- **Absorption:** A + A·B = A ,  A · (A + B) = A
- **De Morgan:** (A·B)' = A' + B' ,  (A+B)' = A' · B'
"""
    )

elif topic == "SOP and POS":
    info_card(
        "Canonical forms",
        "Any Boolean function can be written as Sum-of-Products (SOP) or Product-of-Sums (POS).",
    )
    st.markdown(
        """
**Sum of Products (SOP)** — OR of AND terms. Example: `F = A·B + A'·C`

**Product of Sums (POS)** — AND of OR terms. Example: `F = (A+B)·(A'+C)`

SOP pairs naturally with **minterms** (rows where F = 1).  
POS pairs naturally with **maxterms** (rows where F = 0).
"""
    )

elif topic == "Minterms and Maxterms":
    info_card(
        "Minterms & maxterms",
        "Each row of an n-variable truth table corresponds to one minterm and one maxterm.",
    )
    st.markdown(
        """
For variables A, B:

| A | B | Minterm | Maxterm |
|---|---|---------|---------|
| 0 | 0 | m0 = A'·B' | M0 = A+B |
| 0 | 1 | m1 = A'·B | M1 = A+B' |
| 1 | 0 | m2 = A·B' | M2 = A'+B |
| 1 | 1 | m3 = A·B | M3 = A'+B' |

If `F = Σ(1,3)`, then `F = m1 + m3 = A'·B + A·B`.
"""
    )

else:
    info_card(
        "Karnaugh maps",
        "A K-map rearranges a truth table so adjacent cells (including wrap-around) "
        "differ by one bit (Gray code). Grouping 1s in powers of two yields a simplified SOP.",
    )
    st.markdown(
        """
**Rules**
1. Plot 1s for each minterm (X for don't-cares).
2. Circle largest power-of-two groups (1, 2, 4, 8…).
3. Groups may wrap edges and corners.
4. Each group → one product term; OR all terms for SOP.
5. Don't-cares may join a group if helpful, but never force a group alone.
"""
    )
    st.info("Open **KMap Solver** to select minterms and see automatic grouping.")
