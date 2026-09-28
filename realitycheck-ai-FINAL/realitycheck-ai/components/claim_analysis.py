"""
Claim Analysis Component for REALITYCHECK AI
Displays investigation summary metrics and detailed per-claim evidence breakdowns.
"""

import streamlit as st
from typing import Dict, Any, List

def render_investigation_summary(metrics: Dict[str, Any]):
    """
    Render top summary banner with metrics tiles (Prompt Requirement 11).
    """
    st.markdown("### 📊 Investigation Summary")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-val">{metrics.get("total_claims", 0)}</div>
                <div class="metric-lbl">Total Claims</div>
            </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-val" style="color: #059669;">{metrics.get("supported", 0)}</div>
                <div class="metric-lbl">Supported Claims</div>
            </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-val" style="color: #DC2626;">{metrics.get("conflicting", 0)}</div>
                <div class="metric-lbl">Conflicting Claims</div>
            </div>
        ''', unsafe_allow_html=True)

    with col4:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-val" style="color: #D97706;">{metrics.get("insufficient", 0)}</div>
                <div class="metric-lbl">Insufficient Claims</div>
            </div>
        ''', unsafe_allow_html=True)

    with col5:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-val" style="color: #2563EB;">{metrics.get("total_sources", 0)}</div>
                <div class="metric-lbl">Total Sources</div>
            </div>
        ''', unsafe_allow_html=True)

    with col6:
        st.markdown(f'''
            <div class="metric-card">
                <div class="metric-val" style="color: #7C3AED;">{metrics.get("confidence_score", 0)}%</div>
                <div class="metric-lbl">Overall Confidence</div>
            </div>
        ''', unsafe_allow_html=True)

    # Source Evidence Snippets & Claims Breakdown (Prompt Requirement 4 & 7)
    supp_src = metrics.get("supporting_sources")
    conf_src = metrics.get("conflicting_sources")
    total_src = metrics.get("total_sources", 0)
    total_claims = metrics.get("total_claims", 0)
    supp_claims = metrics.get("supported", 0)
    conf_claims = metrics.get("conflicting", 0)

    if supp_src is not None and conf_src is not None:
        st.markdown(
            f"""
            <div style="font-size: 0.88rem; color: #334155; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.65rem 0.95rem; margin-top: 0.75rem; margin-bottom: 0.4rem; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.6rem;">
                    <div>
                        <b>⚖️ Evaluated Claims ({total_claims} Total):</b> 
                        <span style="color: #059669; font-weight: 700;">{supp_claims} Supported</span> &nbsp;|&nbsp; 
                        <span style="color: #DC2626; font-weight: 700;">{conf_claims} Conflicting</span>
                    </div>
                    <div>
                        <b>🔎 Web Evidence Sources ({total_src} Total):</b> 
                        <span style="color: #059669; font-weight: 700;">{supp_src} Supporting Sources</span> &nbsp;|&nbsp; 
                        <span style="color: #DC2626; font-weight: 700;">{conf_src} Conflicting Sources</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Transparent Confidence Rationale (Prompt Requirement 9)
    if metrics.get("confidence_explanation"):
        st.info(f"**Confidence Rationale ({metrics.get('confidence_score', 0)}%):** {metrics.get('confidence_explanation')}")

def render_claims_breakdown(claims: List[Dict[str, Any]], evidence_list: List[Dict[str, Any]]):
    """
    Render detailed claim cards with supporting & conflicting evidence side-by-side (Prompt Requirement 7).
    """
    st.markdown("### ⚖️ Claim & Evidence Analysis")

    evidence_by_id = {item["id"]: item for item in evidence_list}

    for idx, claim in enumerate(claims, start=1):
        claim_text = claim.get("claim", "")
        status = claim.get("status", "INSUFFICIENT EVIDENCE")
        confidence = claim.get("confidence", "Medium")
        explanation = claim.get("explanation", "")

        supp_ids = claim.get("supporting_evidence_ids", [])
        conf_ids = claim.get("conflicting_evidence_ids", [])

        # Badge styling
        if status == "SUPPORTED":
            badge_html = f'<span class="badge-supported">✓ SUPPORTED</span>'
        elif status == "CONFLICTING":
            badge_html = f'<span class="badge-conflicting">⚠️ CONFLICTING EVIDENCE</span>'
        else:
            badge_html = f'<span class="badge-insufficient">❓ INSUFFICIENT EVIDENCE</span>'

        with st.container():
            st.markdown(
                f'''
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
                        <h4 style="margin: 0; font-size: 1.1rem; color: #0F172A;">Claim #{idx}: {claim_text}</h4>
                        <div>{badge_html} <span style="font-size: 0.8rem; color: #64748B; margin-left: 0.4rem;">(Confidence: <b>{confidence}</b>)</span></div>
                    </div>
                    <p style="font-size: 0.9rem; color: #334155; line-height: 1.5; margin-bottom: 0.8rem;">
                        <b>Analysis Rationale:</b> {explanation}
                    </p>
                </div>
                ''',
                unsafe_allow_html=True
            )

            # Side-by-Side Evidence Columns
            col_supp, col_conf = st.columns(2)

            with col_supp:
                st.markdown("<h5 style='color: #059669; font-size: 0.95rem; margin-bottom: 0.5rem;'>🟢 Supporting Evidence</h5>", unsafe_allow_html=True)
                if supp_ids:
                    for sid in supp_ids:
                        if sid in evidence_by_id:
                            ev = evidence_by_id[sid]
                            st.markdown(
                                f'''
                                <div style="background: #F0FDF4; border-left: 3px solid #10B981; padding: 0.6rem; border-radius: 4px; margin-bottom: 0.5rem; font-size: 0.83rem;">
                                    <b>{ev['source']}</b> <span class="cat-badge cat-official">{ev['category']}</span><br/>
                                    <i>"{ev['snippet']}"</i><br/>
                                    <a href="{ev['link']}" target="_blank" class="evidence-link">🔗 Open Source</a>
                                </div>
                                ''',
                                unsafe_allow_html=True
                            )
                else:
                    st.markdown("<p style='font-size: 0.8rem; color: #94A3B8; italic;'>No direct supporting snippets isolated.</p>", unsafe_allow_html=True)

            with col_conf:
                st.markdown("<h5 style='color: #DC2626; font-size: 0.95rem; margin-bottom: 0.5rem;'>🔴 Conflicting / Counter Evidence</h5>", unsafe_allow_html=True)
                if conf_ids:
                    for cid in conf_ids:
                        if cid in evidence_by_id:
                            ev = evidence_by_id[cid]
                            st.markdown(
                                f'''
                                <div style="background: #FEF2F2; border-left: 3px solid #EF4444; padding: 0.6rem; border-radius: 4px; margin-bottom: 0.5rem; font-size: 0.83rem;">
                                    <b>{ev['source']}</b> <span class="cat-badge cat-community">{ev['category']}</span><br/>
                                    <i>"{ev['snippet']}"</i><br/>
                                    <a href="{ev['link']}" target="_blank" class="evidence-link">🔗 Open Source</a>
                                </div>
                                ''',
                                unsafe_allow_html=True
                            )
                else:
                    st.markdown("<p style='font-size: 0.8rem; color: #94A3B8; italic;'>None found in current search results.</p>", unsafe_allow_html=True)
