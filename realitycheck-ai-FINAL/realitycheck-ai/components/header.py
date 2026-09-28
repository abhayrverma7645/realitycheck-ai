"""
Header component for REALITYCHECK AI
Displays title, tagline, and SerpApi live search indicator.
"""

import streamlit as st
from config import APP_NAME, APP_TAGLINE

def render_header():
    st.markdown(f'<div class="hero-title">🔍 {APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-tagline">"{APP_TAGLINE}"</div>', unsafe_allow_html=True)
    
    # SerpApi Transparency Badge (Prominent UI element)
    st.markdown(
        '''
        <div class="serpapi-badge">
            <span class="serpapi-badge-icon">🌐</span>
            <span>Powered by live web search via <b>SerpApi</b></span>
        </div>
        ''',
        unsafe_allow_html=True
    )
