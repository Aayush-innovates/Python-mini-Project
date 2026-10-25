"""
LogicFlow — Interactive Digital System Design Learning Platform
Learn Logic. Visualize Circuits. Master DSD.
"""

import streamlit as st

from components.ui import apply_theme, module_card, sidebar_brand

st.set_page_config(
    page_title="LogicFlow",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
sidebar_brand()
st.sidebar.success("Select a module from the sidebar navigation.")

st.markdown(
    """
    <div class="logicflow-hero">
        <div class="logicflow-badge">25-Mark Mini Project · Python + Streamlit</div>
        <h1>LogicFlow</h1>
        <p>Interactive Digital System Design Learning Platform — Learn Logic. Visualize Circuits. Master DSD.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Project overview")
st.write(
    "LogicFlow helps engineering students learn Digital System Design through "
    "interactive logic-gate simulation, Boolean simplification, Karnaugh maps, "
    "guided theory pages, and practice quizzes. All computation runs locally in Python; "
    "no database or login is required."
)

st.markdown("### Modules")
col1, col2 = st.columns(2)

with col1:
    module_card(
        "01 · Learn DSD",
        "Concept notes on logic gates, Boolean laws, SOP/POS, minterms/maxterms, and K-Map basics.",
        "Learn",
    )
    module_card(
        "02 · Logic Gate Simulator",
        "Interact with AND, OR, NOT, NAND, NOR, XOR, and XNOR — live outputs and truth tables.",
        "Logic Simulator",
    )
    module_card(
        "03 · Boolean Expression Solver",
        "Enter expressions, validate syntax, simplify with SymPy, and view SOP + truth tables.",
        "Boolean Solver",
    )

with col2:
    module_card(
        "04 · Karnaugh Map Solver",
        "Build 2-, 3-, and 4-variable K-maps, form groups, and generate simplified SOP expressions.",
        "KMap Solver",
    )
    module_card(
        "05 · Quiz & Practice",
        "Topic-based MCQs and short numerical questions with instant feedback and scoring.",
        "Quiz Practice",
    )

st.divider()
st.markdown("### How to use")
st.markdown(
    """
1. Open each module from the **left sidebar**.
2. Try the **Logic Simulator** with different 0/1 inputs.
3. Simplify an expression like `(A+B)*C'` in **Boolean Solver**.
4. Select minterms in **KMap Solver** to see groups and SOP.
5. Test yourself in **Quiz Practice** (score resets when the session ends).
"""
)

st.markdown("### Technology stack")
st.markdown(
    """
| Component | Technology |
|---|---|
| Language | Python 3.11+ |
| UI | Streamlit |
| Boolean algebra | SymPy |
| Visualizations | Streamlit + HTML/SVG |
| Temporary state | Streamlit Session State |
| Testing | pytest |
"""
)

st.caption(
    "Session state resets when the app restarts. No persistent storage or cloud sync."
)
