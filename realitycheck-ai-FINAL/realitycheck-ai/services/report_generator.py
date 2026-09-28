"""
PDF Report Generator for REALITYCHECK AI using ReportLab.
Produces professional, downloadable investigation reports.
"""

import io
import datetime
from typing import Dict, Any, List
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class PDFReportGenerator:
    def generate_pdf(self, investigation_data: Dict[str, Any]) -> bytes:
        """
        Generate a styled PDF report binary buffer for an investigation.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom palette
        PRIMARY = colors.HexColor("#0F172A")    # Dark slate
        SECONDARY = colors.HexColor("#2563EB")  # Vivid blue
        ACCENT_GREEN = colors.HexColor("#059669")# Emerald green
        ACCENT_RED = colors.HexColor("#DC2626")  # Rose red
        ACCENT_AMBER = colors.HexColor("#D97706")# Amber
        BG_GRAY = colors.HexColor("#F8FAFC")     # Soft slate bg
        TEXT_DARK = colors.HexColor("#1E293B")   # Main body text

        # Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=PRIMARY,
            fontName="Helvetica-Bold",
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=13,
            textColor=SECONDARY,
            fontName="Helvetica-Bold",
            spaceAfter=15
        )
        heading2_style = ParagraphStyle(
            "Heading2",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=PRIMARY,
            fontName="Helvetica-Bold",
            spaceBefore=14,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=14,
            textColor=TEXT_DARK,
            fontName="Helvetica"
        )
        meta_label_style = ParagraphStyle(
            "MetaLabel",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#64748B"),
            fontName="Helvetica-Bold"
        )
        meta_val_style = ParagraphStyle(
            "MetaVal",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=PRIMARY,
            fontName="Helvetica"
        )

        story = []

        # 1. Header Banner
        story.append(Paragraph("REALITYCHECK AI", title_style))
        story.append(Paragraph("LIVE WEB EVIDENCE INVESTIGATION REPORT", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=12))

        # 2. Metadata Table
        question = investigation_data.get("question", "N/A")
        date_str = datetime.datetime.now().strftime("%B %d, %Y - %H:%M UTC")
        metrics = investigation_data.get("metrics", {})

        meta_data = [
            [
                Paragraph("<b>TARGET QUERY:</b>", meta_label_style),
                Paragraph(question, meta_val_style)
            ],
            [
                Paragraph("<b>DATE OF INVESTIGATION:</b>", meta_label_style),
                Paragraph(date_str, meta_val_style)
            ],
            [
                Paragraph("<b>SOURCES ANALYZED:</b>", meta_label_style),
                Paragraph(f"{metrics.get('total_sources', 0)} Live Web Results (via SerpApi)", meta_val_style)
            ],
            [
                Paragraph("<b>EVIDENCE CONFIDENCE:</b>", meta_label_style),
                Paragraph(f"<b>{metrics.get('confidence_score', 0)}%</b> - {metrics.get('confidence_explanation', '')}", meta_val_style)
            ]
        ]
        t_meta = Table(meta_data, colWidths=[1.4*inch, 5.8*inch])
        t_meta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_GRAY),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0"))
        ]))
        story.append(t_meta)
        story.append(Spacer(1, 14))

        # 3. Executive Summary
        story.append(Paragraph("1. Executive Summary", heading2_style))
        exec_summary = investigation_data.get("executive_summary", "No summary available.")
        story.append(Paragraph(exec_summary, body_style))
        story.append(Spacer(1, 14))

        # 4. Claims & Verdict Breakdown
        story.append(Paragraph("2. Investigated Factual Claims", heading2_style))
        claims = investigation_data.get("claims", [])
        evidence_dict = {item["id"]: item for item in investigation_data.get("evidence", [])}

        for idx, claim in enumerate(claims, start=1):
            claim_text = claim.get("claim", f"Claim {idx}")
            status = claim.get("status", "INSUFFICIENT EVIDENCE")
            confidence = claim.get("confidence", "Medium")
            explanation = claim.get("explanation", "")

            # Badge color
            if status == "SUPPORTED":
                status_color = ACCENT_GREEN
            elif status == "CONFLICTING":
                status_color = ACCENT_RED
            else:
                status_color = ACCENT_AMBER

            status_p = Paragraph(f"<font color='{status_color.hexval()}'><b>[{status}]</b></font> (Confidence: {confidence})", meta_val_style)
            claim_header_p = Paragraph(f"<b>Claim {idx}:</b> {claim_text}", ParagraphStyle("ClaimH", parent=body_style, fontSize=10, fontName="Helvetica-Bold"))
            
            c_data = [
                [claim_header_p, status_p],
                [Paragraph(f"<b>Analysis & Rationale:</b> {explanation}", body_style), ""]
            ]
            t_claim = Table(c_data, colWidths=[5.4*inch, 1.8*inch])
            t_claim.setStyle(TableStyle([
                ('SPAN', (0,1), (1,1)),
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
                ('PADDING', (0,0), (-1,-1), 8),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LINEBELOW', (0,1), (-1,1), 1, colors.HexColor("#CBD5E1"))
            ]))
            story.append(t_claim)

            # Supporting & Conflicting Evidence details
            supp_ids = claim.get("supporting_evidence_ids", [])
            conf_ids = claim.get("conflicting_evidence_ids", [])

            if supp_ids:
                story.append(Spacer(1, 4))
                story.append(Paragraph("<b>Supporting Evidence:</b>", ParagraphStyle("SuppH", parent=body_style, textColor=ACCENT_GREEN, fontName="Helvetica-Bold")))
                for sid in supp_ids:
                    if sid in evidence_dict:
                        ev = evidence_dict[sid]
                        ev_text = f"• <b>{ev['source']}</b> ({ev['category']}): \"{ev['snippet']}\""
                        story.append(Paragraph(ev_text, ParagraphStyle("EvItem", parent=body_style, leftIndent=12)))

            if conf_ids:
                story.append(Spacer(1, 4))
                story.append(Paragraph("<b>Conflicting / Opposing Evidence:</b>", ParagraphStyle("ConfH", parent=body_style, textColor=ACCENT_RED, fontName="Helvetica-Bold")))
                for cid in conf_ids:
                    if cid in evidence_dict:
                        ev = evidence_dict[cid]
                        ev_text = f"• <b>{ev['source']}</b> ({ev['category']}): \"{ev['snippet']}\""
                        story.append(Paragraph(ev_text, ParagraphStyle("EvItem", parent=body_style, leftIndent=12)))

            story.append(Spacer(1, 10))

        # 5. Methodological Limitations & Transparency
        story.append(Paragraph("3. Assessment & Limitations", heading2_style))
        lim_text = (
            "<b>Transparency Statement:</b> RealityCheck AI retrieves real-time Google search results via SerpApi. "
            "Evidence confidence is evaluated dynamically based on source domain authority, inter-source consensus, "
            "and information directness. Automated analysis does not replace formal expert peer-review."
        )
        story.append(Paragraph(lim_text, body_style))
        story.append(Spacer(1, 14))

        # 6. Source Index
        story.append(Paragraph("4. Analyzed Sources Appendix", heading2_style))
        evidence_list = investigation_data.get("evidence", [])
        
        src_table_data = [
            [Paragraph("<b>Source</b>", meta_label_style), Paragraph("<b>Category</b>", meta_label_style), Paragraph("<b>Snippet / Evidence</b>", meta_label_style)]
        ]
        for ev in evidence_list[:15]:
            src_str = f"<a href='{ev['link']}'><u>{ev['source']}</u></a>"
            src_table_data.append([
                Paragraph(src_str, body_style),
                Paragraph(ev["category"], body_style),
                Paragraph(ev["snippet"][:140] + "...", body_style)
            ])

        t_src = Table(src_table_data, colWidths=[1.8*inch, 1.1*inch, 4.3*inch])
        t_src.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        story.append(t_src)

        # Build document
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
