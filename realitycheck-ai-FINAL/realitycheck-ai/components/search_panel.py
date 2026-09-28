"""
Search Panel Component for REALITYCHECK AI
Handles search input, example query buttons, and live investigation progress tracking.
"""

import streamlit as st
from typing import Tuple, Optional

EXAMPLE_QUERIES = [
    "Is this laptop worth buying in 2026?",
    "Are electric vehicles cheaper to own than petrol cars?",
    "What are the current software engineering career opportunities?",
    "Is this viral claim supported by reliable sources?"
]

def render_search_panel() -> Tuple[str, bool]:
    """
    Render search input bar and example query buttons.
    Returns (query_string, is_submitted).
    """
    if "input_query" not in st.session_state:
        st.session_state["input_query"] = ""

    # Prominent unified Search Bar layout
    col_input, col_btn = st.columns([3.8, 1.2], vertical_alignment="bottom")
    
    with col_input:
        query = st.text_input(
            label="Enter Question, Claim, or Product Query for Live Investigation:",
            value=st.session_state.get("input_query", ""),
            placeholder="e.g. Are electric vehicles cheaper to maintain than gas cars over 5 years?",
            key="search_input_box"
        )

    with col_btn:
        submitted = st.button("🚀 Investigate Claim", type="primary", use_container_width=True)

    # Example query pill buttons (Prompt Requirement 15)
    st.markdown("<p style='font-size: 0.85rem; color: #64748B; margin-top: 0.7rem; margin-bottom: 0.3rem;'><b>Try an Example Investigation:</b></p>", unsafe_allow_html=True)
    
    cols = st.columns(len(EXAMPLE_QUERIES))
    selected_example = None

    for idx, ex in enumerate(EXAMPLE_QUERIES):
        with cols[idx]:
            if st.button(ex, key=f"ex_btn_{idx}", use_container_width=True):
                selected_example = ex

    if selected_example:
        st.session_state["input_query"] = selected_example
        query = selected_example
        submitted = True

    return query, submitted

def render_progress_box(current_step: int, status_messages: dict):
    """
    Render visible 6-step progress container (Prompt Requirement 5).
    """
    steps = [
        (1, "Understanding question"),
        (2, "Generating investigation queries"),
        (3, "Searching live web via SerpApi"),
        (4, "Collecting evidence"),
        (5, "Checking conflicting evidence"),
        (6, "Generating investigation report")
    ]

    st.markdown('<div class="progress-box">', unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; font-size: 1rem; color: #1E293B;'>⚡ Live Investigation Progress:</h4>", unsafe_allow_html=True)

    for step_num, step_name in steps:
        if step_num < current_step:
            icon = '<span class="progress-check">✓</span>'
            status_style = 'color: #059669; font-weight: 600;'
            msg = status_messages.get(step_num, f"{step_name} ✓")
        elif step_num == current_step:
            icon = '<span class="progress-spin">⏳</span>'
            status_style = 'color: #2563EB; font-weight: 700;'
            msg = status_messages.get(step_num, f"{step_name}...")
        else:
            icon = '<span style="color: #94A3B8;">○</span>'
            status_style = 'color: #94A3B8;'
            msg = step_name

        st.markdown(
            f'''
            <div class="progress-item">
                {icon}
                <span style="{status_style}">STEP {step_num}: {msg}</span>
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
