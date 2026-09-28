"""
Custom CSS Styles for REALITYCHECK AI
Implements modern SaaS design system, glassmorphism, responsive cards, and vibrant badges.
"""

import streamlit as st

def inject_custom_styles():
    st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding - Reduced unnecessary top whitespace */
    .block-container {
        padding-top: 1.0rem;
        padding-bottom: 2.5rem;
        max-width: 1200px;
    }

    /* SaaS Hero Header */
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 2.7rem;
        background: linear-gradient(135deg, #0F172A 0%, #2563EB 50%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.04em;
        margin-bottom: 0.15rem;
        line-height: 1.1;
    }

    .hero-tagline {
        font-size: 1.05rem;
        color: #475569;
        font-weight: 500;
        margin-bottom: 0.8rem;
    }

    /* Prominent SerpApi Transparency Badge */
    .serpapi-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        border: 1.5px solid rgba(37, 99, 235, 0.35);
        color: #1D4ED8;
        padding: 0.45rem 1.0rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.12);
    }
    .serpapi-badge-icon {
        font-size: 1.0rem;
    }

    /* Prominent Search Input Box Styling */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
        border: 2px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #2563EB !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.2) !important;
    }
    div[data-baseweb="input"] input {
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        color: #0F172A !important;
        padding: 0.65rem 0.9rem !important;
    }

    /* Prominent Investigate Primary Button */
    div.stButton > button[kind="primary"], div.stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.0rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45) !important;
        transform: translateY(-1px) !important;
    }

    /* Example Query Buttons Styling */
    div.stButton > button:not([kind="primary"]) {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.65rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        text-align: left !important;
        height: 100% !important;
    }
    div.stButton > button:not([kind="primary"]):hover {
        border-color: #2563EB !important;
        color: #2563EB !important;
        background-color: #F8FAFC !important;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .metric-val {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
    }
    .metric-lbl {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.2rem;
    }

    /* Status Badges */
    .badge-supported {
        background-color: #DEF7EC;
        color: #03543F;
        border: 1px solid #84E1BC;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-conflicting {
        background-color: #FDE8E8;
        color: #9B1C1C;
        border: 1px solid #F8B4B4;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-insufficient {
        background-color: #FEF08A;
        color: #713F12;
        border: 1px solid #FDE047;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }

    /* Category Badges */
    .cat-official { background: #E0F2FE; color: #0369A1; }
    .cat-research { background: #F3E8FF; color: #6B21A8; }
    .cat-news { background: #FEF3C7; color: #92400E; }
    .cat-review { background: #DCFCE7; color: #166534; }
    .cat-industry { background: #E0E7FF; color: #3730A3; }
    .cat-community { background: #FFE4E6; color: #9F1239; }
    .cat-other { background: #F1F5F9; color: #475569; }

    .cat-badge {
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Evidence Card */
    .evidence-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .evidence-title {
        font-weight: 700;
        font-size: 0.95rem;
        color: #1E293B;
        margin-bottom: 0.3rem;
    }
    .evidence-snippet {
        font-size: 0.85rem;
        color: #475569;
        line-height: 1.4;
        margin-bottom: 0.5rem;
    }
    .evidence-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.78rem;
        color: #94A3B8;
    }
    .evidence-link {
        color: #2563EB !important;
        font-weight: 600;
        text-decoration: none;
    }
    .evidence-link:hover {
        text-decoration: underline;
    }

    /* Progress Tracker Card */
    .progress-box {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.8rem 0;
    }
    .progress-item {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.9rem;
        color: #334155;
        padding: 0.25rem 0;
    }
    .progress-check {
        color: #10B981;
        font-weight: bold;
    }
    .progress-spin {
        color: #2563EB;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
