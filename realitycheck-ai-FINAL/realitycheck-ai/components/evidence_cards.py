"""
Evidence Cards Component for REALITYCHECK AI
Grid display of individual source snippets with category badges and source links.
"""

import streamlit as st
from typing import List, Dict, Any

def render_evidence_cards(evidence_list: List[Dict[str, Any]]):
    """
    Render grid of structured evidence cards (Prompt Requirement 12).
    """
    st.markdown("### 📚 Live Search Evidence Explorer")

    if not evidence_list:
        st.info("No evidence items available.")
        return

    # Filter by source category selector
    categories = ["All"] + sorted(list(set(ev.get("category", "Other") for ev in evidence_list)))
    selected_cat = st.selectbox("Filter Sources by Category:", categories, key="ev_cat_filter")

    filtered_list = evidence_list
    if selected_cat != "All":
        filtered_list = [ev for ev in evidence_list if ev.get("category") == selected_cat]

    st.markdown(f"<p style='font-size: 0.85rem; color: #64748B;'>Displaying <b>{len(filtered_list)}</b> live search results:</p>", unsafe_allow_html=True)

    # Render in 2 columns
    col1, col2 = st.columns(2)

    for idx, item in enumerate(filtered_list):
        category = item.get("category", "Other")
        cat_class = f"cat-{category.lower()}"
        date_str = f" • {item['date']}" if item.get("date") else ""
        link = item.get("link", "#")

        card_html = f'''
        <div class="evidence-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.3rem;">
                <span class="cat-badge {cat_class}">{category}</span>
                <span style="font-size: 0.75rem; color: #94A3B8;">{item.get("result_type", "Web")}{date_str}</span>
            </div>
            <div class="evidence-title">{item['title']}</div>
            <div class="evidence-snippet">"{item['snippet']}"</div>
            <div class="evidence-footer">
                <span><b>Source:</b> {item['source']} ({item['domain']})</span>
                <a href="{link}" target="_blank" class="evidence-link">🔗 Open Source</a>
            </div>
        </div>
        '''

        if idx % 2 == 0:
            with col1:
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(card_html, unsafe_allow_html=True)
