"""Shared UI helpers and theme for LogicFlow."""

import streamlit as st

NAVY = "#0A2540"
ACCENT = "#1B4F72"
LIGHT_GRAY = "#F4F6F8"
WHITE = "#FFFFFF"
BORDER = "#D0D7DE"


def apply_theme():
    """Inject navy / white / light-gray styling across the app."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {LIGHT_GRAY};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {NAVY};
        }}
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] small {{
            color: {WHITE} !important;
        }}
        /* Keep page nav readable */
        [data-testid="stSidebarNav"] a {{
            color: {WHITE} !important;
            background: transparent;
        }}
        [data-testid="stSidebarNav"] a:hover {{
            background: rgba(255,255,255,0.12) !important;
        }}
        [data-testid="stSidebarNav"] [aria-selected="true"] a,
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: rgba(255,255,255,0.18) !important;
            border-left: 3px solid #7DD3FC;
        }}
        h1, h2, h3 {{
            color: {NAVY} !important;
        }}
        .logicflow-card {{
            background: {WHITE};
            border: 1px solid {BORDER};
            border-radius: 10px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(10, 37, 64, 0.08);
        }}
        .logicflow-card h3 {{
            margin-top: 0;
            color: {NAVY};
        }}
        .logicflow-card p {{
            color: #334155;
            margin-bottom: 0;
        }}
        .logicflow-hero {{
            background: linear-gradient(135deg, {NAVY} 0%, {ACCENT} 100%);
            color: {WHITE};
            border-radius: 12px;
            padding: 2rem 2.25rem;
            margin-bottom: 1.5rem;
        }}
        .logicflow-hero h1 {{
            color: {WHITE} !important;
            margin: 0 0 0.5rem 0;
            font-size: 2rem;
        }}
        .logicflow-hero p {{
            color: rgba(255,255,255,0.92);
            margin: 0;
            font-size: 1.05rem;
        }}
        .logicflow-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.15);
            color: {WHITE};
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.8rem;
            margin-bottom: 0.75rem;
        }}
        .bit-on {{
            display:inline-block;padding:8px 18px;border-radius:8px;
            background:#D8F3E3;color:#0E5C36;font-weight:700;font-size:1.4rem;
        }}
        .bit-off {{
            display:inline-block;padding:8px 18px;border-radius:8px;
            background:#EEF2F6;color:#475569;font-weight:700;font-size:1.4rem;
        }}
        div.stButton > button {{
            background-color: {NAVY};
            color: {WHITE};
            border: none;
            border-radius: 6px;
        }}
        div.stButton > button:hover {{
            background-color: {ACCENT};
            color: {WHITE};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    st.sidebar.markdown("### LogicFlow")
    st.sidebar.caption("Digital System Design Lab")
    st.sidebar.markdown("---")


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)
    st.divider()


def info_card(title: str, body: str):
    st.markdown(
        f"""
        <div class="logicflow-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def module_card(title: str, description: str, page_hint: str):
    st.markdown(
        f"""
        <div class="logicflow-card">
            <h3>{title}</h3>
            <p>{description}</p>
            <p style="margin-top:0.75rem;color:#1B4F72;font-size:0.9rem;">
                Open from the sidebar → <strong>{page_hint}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bit_badge(value: int) -> str:
    cls = "bit-on" if value == 1 else "bit-off"
    return f'<span class="{cls}">{value}</span>'
