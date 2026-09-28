"""
REALITYCHECK AI - Live Web Investigation Platform
Main Streamlit Application File
"""

import streamlit as st
import pandas as pd
import json
import os

from config import APP_NAME, APP_TAGLINE, SERPAPI_KEY, LLM_API_KEY
from components.styles import inject_custom_styles
from components.header import render_header
from components.search_panel import render_search_panel, render_progress_box
from components.claim_analysis import render_investigation_summary, render_claims_breakdown
from components.evidence_cards import render_evidence_cards
from components.evidence_graph import render_evidence_graph

from services.investigation_engine import InvestigationEngine
from services.history_service import HistoryService
from services.report_generator import PDFReportGenerator
from services.serpapi_service import SerpApiService

# Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} | Live Web Investigation Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom SaaS CSS Styles
inject_custom_styles()

# Initialize Session State Variables
if "current_investigation" not in st.session_state:
    st.session_state["current_investigation"] = None

if "runtime_serpapi_key" not in st.session_state:
    st.session_state["runtime_serpapi_key"] = SERPAPI_KEY

if "runtime_llm_key" not in st.session_state:
    st.session_state["runtime_llm_key"] = LLM_API_KEY

# Initialize Services
history_service = HistoryService()
pdf_generator = PDFReportGenerator()

# ==============================================================================
# SIDEBAR NAVIGATION & SETTINGS (Prompt Requirement 4)
# ==============================================================================
with st.sidebar:
    st.markdown(f"## 🔍 {APP_NAME}")
    st.caption(f'"{APP_TAGLINE}"')
    st.divider()

    # Navigation Radio
    nav_option = st.radio(
        "Navigation",
        options=["✨ New Investigation", "📜 Investigation History", "ℹ️ About RealityCheck"],
        index=0
    )

    st.divider()

    # Sidebar Settings & API Keys
    with st.expander("🔑 API Key Settings", expanded=False):
        st.markdown("<p style='font-size: 0.8rem; color: #64748B;'>Configure or override API keys for live investigation:</p>", unsafe_allow_html=True)
        
        user_serp_key = st.text_input(
            "SerpApi Key:",
            value=st.session_state["runtime_serpapi_key"],
            type="password",
            help="Required for live web search via SerpApi."
        )
        if user_serp_key != st.session_state["runtime_serpapi_key"]:
            st.session_state["runtime_serpapi_key"] = user_serp_key

        user_llm_key = st.text_input(
            "LLM API Key (Optional):",
            value=st.session_state["runtime_llm_key"],
            type="password",
            help="OpenAI / Gemini / LiteLLM key for AI claim extraction. (Heuristic NLP fallback enabled if empty)"
        )
        if user_llm_key != st.session_state["runtime_llm_key"]:
            st.session_state["runtime_llm_key"] = user_llm_key

        # Key Status Indicators
        serp_active = bool(st.session_state["runtime_serpapi_key"].strip())
        llm_active = bool(st.session_state["runtime_llm_key"].strip())

        st.markdown(
            f"""
            <div style="font-size: 0.78rem; margin-top: 0.5rem;">
                SerpApi Search: <b>{'🟢 Configured' if serp_active else '🔴 Missing Key'}</b><br/>
                LLM Analysis: <b>{'🟢 Configured' if llm_active else '🟡 Rule-Based Fallback'}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown(
        """
        <div style="font-size: 0.75rem; color: #94A3B8; text-align: center;">
            SerpApi Hackathon Submission 2026<br/>
            Built with Streamlit & Plotly
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# PAGE 1: NEW INVESTIGATION
# ==============================================================================
if nav_option == "✨ New Investigation":
    render_header()

    query, submitted = render_search_panel()

    # Handle Search Submission
    if submitted:
        if not query.strip():
            st.warning("⚠️ Please enter a question or claim to start the investigation.")
        else:
            # Check SerpApi Key
            active_serp_key = st.session_state["runtime_serpapi_key"].strip() or SERPAPI_KEY
            if not active_serp_key or active_serp_key == "your_serpapi_key_here":
                st.error(
                    "❌ **SerpApi Key is Missing.**\n\n"
                    "Please provide a valid `SERPAPI_KEY` in your `.env` file or enter it in the **Sidebar -> 🔑 API Key Settings**."
                )
            else:
                progress_container = st.empty()
                status_dict = {}

                def update_progress(step: int, text: str, done: bool):
                    status_dict[step] = text
                    with progress_container.container():
                        render_progress_box(step, status_dict)

                # Initialize Engine and Execute Pipeline
                engine = InvestigationEngine(
                    serpapi_key=active_serp_key,
                    llm_key=st.session_state["runtime_llm_key"].strip() or LLM_API_KEY
                )

                with st.spinner("Running live web investigation..."):
                    result = engine.run_investigation(query, progress_callback=update_progress)

                # Clear progress box container after completion
                progress_container.empty()

                if not result.get("success"):
                    st.error(f"❌ **Investigation Error:** {result.get('error')}")
                else:
                    st.session_state["current_investigation"] = result
                    st.success("✅ Investigation completed successfully!")

    # Render Current Investigation Results
    inv_data = st.session_state.get("current_investigation")

    if inv_data:
        st.divider()

        # Top Bar: Executive Summary & PDF Report Download Button (Prompt Requirement 14)
        col_hdr, col_dl = st.columns([3, 1])

        with col_hdr:
            st.markdown(f"### 📑 Investigation Report: *\"{inv_data['question']}\"*")
            st.markdown(f"**Executive Summary:** {inv_data['executive_summary']}")

        with col_dl:
            # Generate PDF binary
            try:
                pdf_bytes = pdf_generator.generate_pdf(inv_data)
                clean_q_name = "".join(c if c.isalnum() else "_" for c in inv_data['question'][:20])
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"RealityCheck_Report_{clean_q_name}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.warning(f"Unable to generate PDF report: {e}")

        st.markdown("<br/>", unsafe_allow_html=True)

        # Investigation Metrics Summary Banner (Prompt Requirement 11)
        render_investigation_summary(inv_data["metrics"])

        st.markdown("<br/>", unsafe_allow_html=True)

        # Tabs for Evidence Breakdown, Interactive Graph, Evidence Explorer & Raw Queries
        tab1, tab2, tab3, tab4 = st.tabs([
            "⚖️ Claims & Evidence",
            "🕸️ Interactive Evidence Graph",
            "📚 Live Evidence Explorer",
            "🔍 SerpApi Queries & Metadata"
        ])

        with tab1:
            render_claims_breakdown(inv_data["claims"], inv_data["evidence"])

        with tab2:
            render_evidence_graph(inv_data)

        with tab3:
            render_evidence_cards(inv_data["evidence"])

        with tab4:
            st.markdown("### 🔍 Live SerpApi Execution Details")
            st.markdown(f"**Primary Question:** `{inv_data['question']}`")
            st.markdown("**Executed Search Queries:**")
            for q in inv_data.get("queries_used", []):
                st.code(f"SerpApi Google Search: q='{q}'", language="bash")

            st.markdown(f"**Total Raw Search Items Retained:** `{len(inv_data.get('evidence', []))}`")


# ==============================================================================
# PAGE 2: INVESTIGATION HISTORY (Prompt Requirement 13)
# ==============================================================================
elif nav_option == "📜 Investigation History":
    st.markdown("## 📜 Local Investigation History")
    st.caption("Re-open past investigations without calling external APIs again.")

    history_records = history_service.get_history(limit=50)

    if not history_records:
        st.info("No past investigations saved in local database yet. Perform a new investigation to build history!")
    else:
        st.markdown(f"Found **{len(history_records)}** past investigations:")

        for rec in history_records:
            with st.container():
                col_info, col_act = st.columns([4, 1])

                with col_info:
                    verdict = rec.get("verdict", "UNVERIFIED")
                    v_color = "#059669" if verdict == "SUPPORTED" else ("#DC2626" if verdict == "CONFLICTING" else "#D97706")
                    
                    st.markdown(
                        f"""
                        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.9rem; margin-bottom: 0.6rem;">
                            <div style="display: flex; justify-content: space-between;">
                                <h4 style="margin:0; font-size: 1rem; color: #0F172A;">{rec['question']}</h4>
                                <span style="font-size: 0.8rem; color: {v_color}; font-weight: bold;">[{verdict}]</span>
                            </div>
                            <p style="font-size: 0.82rem; color: #64748B; margin: 0.3rem 0 0.5rem 0;">
                                📅 <i>{rec['timestamp']}</i> • 📊 {rec['total_sources']} Sources • ⚖️ {rec['total_claims']} Claims • Confidence: <b>{rec['confidence_score']}%</b>
                            </p>
                            <p style="font-size: 0.85rem; color: #334155; margin: 0;">{rec['summary'][:160]}...</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col_act:
                    if st.button("📂 Re-open", key=f"reopen_{rec['id']}", use_container_width=True):
                        full_payload = history_service.get_investigation_by_id(rec['id'])
                        if full_payload:
                            st.session_state["current_investigation"] = full_payload
                            st.success("Investigation loaded! Navigating to New Investigation page...")
                            st.rerun()

                    if st.button("🗑️ Delete", key=f"del_{rec['id']}", use_container_width=True):
                        history_service.delete_investigation(rec['id'])
                        st.rerun()


# ==============================================================================
# PAGE 3: ABOUT REALITYCHECK
# ==============================================================================
elif nav_option == "ℹ️ About RealityCheck":
    st.markdown("## ℹ️ About REALITYCHECK AI")
    st.markdown(
        """
        > **"Search engines give you results. RealityCheck turns those results into an investigation."**

        **REALITYCHECK AI** is an AI-powered live-web investigation platform created for the **SerpApi Hackathon**.
        
        ### 🎯 Problem Statement
        Traditional search engines return lists of blue links. When users try to evaluate complex claims, buying decisions, or viral news, they are forced to open dozens of tabs, manually compare conflicting articles, and guess which sources are trustworthy.

        ### ⚡ How RealityCheck Works
        1. **Intent Understanding**: Deconstructs user queries into target claims.
        2. **Multi-Perspective Search**: Generates supporting and counter-evidence search queries.
        3. **Live SerpApi Search**: Fetches live web results from Google Search using SerpApi.
        4. **Source Classification**: Categorizes sources into *Official, News, Research, Industry, Review, Community*.
        5. **Conflict Detection**: Explicitly isolates contradicting evidence alongside supporting evidence.
        6. **Transparent Confidence**: Calculates a multi-factor confidence rating without scientific pretense.
        7. **Interactive Visualization**: Builds Plotly network graphs mapping Question → Claims → Sources.
        8. **PDF Export**: Produces publication-grade PDF investigation reports.

        ---

        ### 🌐 Powered by SerpApi
        RealityCheck uses SerpApi as its core data pipeline engine to access real-time web search results cleanly, reliably, and without rate limit interruptions.
        """
    )
