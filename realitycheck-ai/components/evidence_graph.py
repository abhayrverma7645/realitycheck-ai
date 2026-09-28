"""
Interactive Plotly Evidence Graph Component for REALITYCHECK AI
Visualizes relationship hierarchy: Question -> Claims -> Evidence / Sources.
"""

import plotly.graph_objects as go
import streamlit as st
from typing import Dict, Any, List

def get_short_source_label(source: str, domain: str) -> str:
    """
    Format source names into clean, readable short labels to prevent graph clutter.
    """
    s_lower = (source or "").lower()
    d_lower = (domain or "").lower()

    if "energy.gov" in d_lower or "doe" in s_lower or "department of energy" in s_lower:
        return "US DOE"
    if "nih.gov" in d_lower or "nih" in s_lower or "national institutes of health" in s_lower:
        return "NIH"
    if "cdc.gov" in d_lower or "cdc" in s_lower:
        return "CDC"
    if "mayo" in d_lower or "mayo" in s_lower:
        return "Mayo Clinic"
    if "harvard" in d_lower or "harvard" in s_lower:
        return "Harvard"
    if "consumerreports" in d_lower or "consumer reports" in s_lower:
        return "Consumer Reports"
    if "reuters" in d_lower or "reuters" in s_lower:
        return "Reuters"
    if "bloomberg" in d_lower or "bloomberg" in s_lower:
        return "Bloomberg"
    if "nytimes" in d_lower or "new york times" in s_lower:
        return "NY Times"
    if "wsj" in d_lower or "wall street journal" in s_lower:
        return "WSJ"
    if "bbc" in d_lower or "bbc" in s_lower:
        return "BBC News"
    if "who.int" in d_lower or "world health" in s_lower:
        return "WHO"
    if "nasa" in d_lower or "nasa" in s_lower:
        return "NASA"
    if "arxiv" in d_lower or "arxiv" in s_lower:
        return "arXiv"
    if "nature.com" in d_lower or "nature" in s_lower:
        return "Nature"
    if "reddit" in d_lower or "reddit" in s_lower:
        return "Reddit"

    cleaned = (source or "").strip()
    if ":" in cleaned:
        cleaned = cleaned.split(":")[0].strip()
    if "-" in cleaned and len(cleaned) > 18:
        cleaned = cleaned.split("-")[0].strip()

    if len(cleaned) > 16:
        cleaned = cleaned[:14] + ".."
    return cleaned if cleaned else (domain or "Source")


def render_evidence_graph(investigation_data: Dict[str, Any]):
    """
    Render interactive Plotly evidence network graph.
    Hierarchy: Question (top) -> Claims (middle) -> Evidence / Sources (bottom).
    """
    st.markdown("### 🕸️ Interactive Evidence & Source Graph")
    st.caption("Visualizing hierarchical relationship from Question → Claims → Evidence Items → Web Sources")

    question = investigation_data.get("question", "Question")
    claims = investigation_data.get("claims", [])
    evidence_list = investigation_data.get("evidence", [])
    evidence_by_id = {item["id"]: item for item in evidence_list}

    nodes = []
    edges = []

    # Node 0: Question (Top Center)
    q_label = f"Question: {question[:38]}..." if len(question) > 38 else f"Question: {question}"
    nodes.append({
        "id": "Q0",
        "label": q_label,
        "full_text": f"Question: {question}",
        "type": "Question",
        "color": "#2563EB",  # Vivid Blue
        "size": 34,
        "x": 0.0,
        "y": 1.1
    })

    # Level 2: Claims
    num_claims = len(claims)
    for c_idx, claim in enumerate(claims):
        c_node_id = f"C{c_idx}"
        status = claim.get("status", "INSUFFICIENT EVIDENCE")

        if status == "SUPPORTED":
            color = "#059669"  # Emerald
        elif status == "CONFLICTING":
            color = "#DC2626"  # Red
        else:
            color = "#D97706"  # Amber

        # Horizontal placement for claims
        if num_claims == 1:
            c_x = 0.0
        elif num_claims == 2:
            c_x = -0.65 if c_idx == 0 else 0.65
        else:
            c_x_start = -0.75
            c_x_step = 1.5 / max(1, num_claims - 1)
            c_x = c_x_start + (c_idx * c_x_step)

        c_y = 0.45

        c_text_short = claim.get('claim', '')
        if len(c_text_short) > 32:
            c_text_short = c_text_short[:30] + ".."

        nodes.append({
            "id": c_node_id,
            "label": f"Claim #{c_idx+1}: {c_text_short}",
            "full_text": f"Status: {status}<br>Claim #{c_idx+1}: {claim.get('claim', '')}<br>Rationale: {claim.get('explanation', '')}",
            "type": f"Claim ({status})",
            "color": color,
            "size": 26,
            "x": c_x,
            "y": c_y
        })

        # Connect Question -> Claim
        edges.append(("Q0", c_node_id, "#CBD5E1"))

        # Level 3: Evidence Nodes attached to Claim
        supp_ids = claim.get("supporting_evidence_ids", [])
        conf_ids = claim.get("conflicting_evidence_ids", [])

        all_ev_ids = [(sid, "SUPPORTED") for sid in supp_ids] + [(cid, "CONFLICTING") for cid in conf_ids]
        ev_items_to_render = all_ev_ids[:5]  # Limit to 5 per claim for crisp visibility
        n_ev = len(ev_items_to_render)

        if n_ev > 0:
            if num_claims == 1:
                sub_x_min, sub_x_max = -0.85, 0.85
            elif num_claims == 2:
                sub_x_min, sub_x_max = (-1.1, -0.2) if c_idx == 0 else (0.2, 1.1)
            else:
                sub_x_width = 1.4 / num_claims
                sub_x_min = c_x - (sub_x_width / 2)
                sub_x_max = c_x + (sub_x_width / 2)

            ev_x_step = (sub_x_max - sub_x_min) / max(1, n_ev - 1) if n_ev > 1 else 0

            for e_idx, (ev_id, rel_status) in enumerate(ev_items_to_render):
                if ev_id in evidence_by_id:
                    ev_item = evidence_by_id[ev_id]
                    e_node_id = f"E_{c_idx}_{ev_id}"
                    ev_color = "#10B981" if rel_status == "SUPPORTED" else "#EF4444"

                    ev_x = sub_x_min + (e_idx * ev_x_step) if n_ev > 1 else c_x
                    # Stagger y position between upper bottom (-0.25) and lower bottom (-0.68)
                    ev_y = -0.25 if (e_idx % 2 == 0) else -0.68

                    short_name = get_short_source_label(ev_item.get("source", ""), ev_item.get("domain", ""))

                    nodes.append({
                        "id": e_node_id,
                        "label": short_name,
                        "full_text": f"<b>Full Source:</b> {ev_item.get('source', 'Web Source')}<br><b>Category:</b> {ev_item.get('category', 'Web')}<br><b>Snippet:</b> \"{ev_item.get('snippet', '')[:120]}...\"",
                        "type": f"Evidence ({rel_status})",
                        "color": ev_color,
                        "size": 18,
                        "x": ev_x,
                        "y": ev_y
                    })

                    # Edge Claim -> Evidence
                    edges.append((c_node_id, e_node_id, ev_color))

    # Build Plotly Figure
    edge_x = []
    edge_y = []
    node_dict = {n["id"]: n for n in nodes}

    for src_id, tgt_id, edge_col in edges:
        if src_id in node_dict and tgt_id in node_dict:
            src = node_dict[src_id]
            tgt = node_dict[tgt_id]
            edge_x.extend([src["x"], tgt["x"], None])
            edge_y.extend([src["y"], tgt["y"], None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='#CBD5E1'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = [n["x"] for n in nodes]
    node_y = [n["y"] for n in nodes]
    node_text = [n["label"] for n in nodes]
    node_hover = [n["full_text"] for n in nodes]
    node_colors = [n["color"] for n in nodes]
    node_sizes = [n["size"] for n in nodes]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        hovertext=node_hover,
        text=node_text,
        textposition="bottom center",
        textfont=dict(size=11, family="Inter, sans-serif", color="#1E293B"),
        marker=dict(
            showscale=False,
            color=node_colors,
            size=node_sizes,
            line=dict(width=2, color='#FFFFFF')
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=30, l=30, r=30, t=30),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.25, 1.25]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.95, 1.3]),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500
        )
    )

    st.plotly_chart(fig, use_container_width=True)
