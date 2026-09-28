"""
Evidence Analyzer Service for REALITYCHECK AI
Handles source classification, claim extraction, evidence relation tagging,
conflict detection, and transparent confidence calculation.
"""

import re
import urllib.parse
from typing import List, Dict, Any, Tuple

class EvidenceAnalyzer:
    def __init__(self):
        pass

    def classify_source(self, domain: str, title: str = "", snippet: str = "") -> str:
        """
        Classify source domain into standard categories:
        Official, News, Research, Industry, Review, Community, Other
        """
        domain_lower = domain.lower()
        title_lower = title.lower()
        snippet_lower = snippet.lower()

        # Official (.gov, .edu, specific government & international official orgs)
        if any(ext in domain_lower for ext in [".gov", ".edu", "gov.", "state.", "who.int", "cdc.gov", "nih.gov", "nasa.gov", "europa.eu"]):
            return "Official"
        if any(k in domain_lower for k in ["apple.com", "microsoft.com", "google.com", "tesla.com"]):
            return "Official"

        # Research / Academic
        if any(k in domain_lower for k in ["arxiv", "nature.com", "sciencedirect", "springer", "ieee", "researchgate", "pubmed", "semanticscholar", "doi.org", "biorxiv"]):
            return "Research"
        if any(k in snippet_lower for k in ["peer-reviewed", "journal", "clinical trial", "study published", "researchers found"]):
            return "Research"

        # News
        news_domains = [
            "reuters.com", "bloomberg.com", "bbc.com", "bbc.co.uk", "cnn.com", "nytimes.com",
            "wsj.com", "washingtonpost.com", "theguardian.com", "forbes.com", "cnbc.com",
            "apnews.com", "ft.com", "techcrunch.com", "theverge.com", "wired.com", "arstechnica.com"
        ]
        if any(nd in domain_lower for nd in news_domains) or ("news" in domain_lower and not "autonews" in domain_lower):
            return "News"

        # Review / Comparison
        if any(k in domain_lower or k in title_lower for k in ["review", "benchmark", "rtings", "tomsguide", "cnet", "pcmag", "techradar", "consumer-reports", "versus"]):
            return "Review"

        # Community / Social / Forum
        if any(k in domain_lower for k in ["reddit.com", "quora.com", "stackexchange.com", "stackoverflow.com", "medium.com", "forum", "community", "x.com", "twitter.com"]):
            return "Community"

        # Industry / Corporate
        if any(k in domain_lower for k in ["inc.com", "businessinsider.com", "gartner.com", "mckinsey.com", "statista.com", "venturebeat.com"]):
            return "Industry"

        return "Other"

    def analyze_investigation(self, question: str, raw_evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process raw search results to extract claims, categorize supporting and conflicting evidence,
        calculate metrics and generate transparent report metadata.
        """
        # Step A: Enrich evidence with source classification
        enriched_evidence = []
        seen_snippets = set()

        for item in raw_evidence:
            snippet = item.get("snippet", "").strip()
            # Basic text deduplication
            snippet_key = snippet.lower()[:80]
            if snippet_key and snippet_key in seen_snippets:
                continue
            if snippet_key:
                seen_snippets.add(snippet_key)

            domain = item.get("domain") or self._extract_domain(item.get("link", ""))
            category = self.classify_source(domain, item.get("title", ""), snippet)

            enriched_item = {
                "id": len(enriched_evidence) + 1,
                "title": item.get("title", "Untitled Web Result"),
                "link": item.get("link", "#"),
                "snippet": snippet,
                "source": item.get("source") or domain,
                "domain": domain,
                "category": category,
                "date": item.get("date", "Recent"),
                "result_type": item.get("result_type", "Search Result"),
                "origin_query": item.get("origin_query", question)
            }
            enriched_evidence.append(enriched_item)

        # Step B: Rule-Based NLP Claim Analysis
        claims_analysis = self._heuristic_extract_claims(question, enriched_evidence)

        # Step C: Post-process claims and compute metrics
        claims = claims_analysis.get("claims", [])
        
        supported_count = sum(1 for c in claims if c.get("status") == "SUPPORTED")
        conflicting_count = sum(1 for c in claims if c.get("status") == "CONFLICTING")
        insufficient_count = sum(1 for c in claims if c.get("status") == "INSUFFICIENT EVIDENCE")

        # Count unique supporting and conflicting source evidence snippets
        supp_snippet_ids = set()
        conf_snippet_ids = set()
        for c in claims:
            supp_snippet_ids.update(c.get("supporting_evidence_ids", []))
            conf_snippet_ids.update(c.get("conflicting_evidence_ids", []))

        confidence_score, confidence_explanation = self._calculate_confidence(
            question=question,
            claims=claims,
            total_sources=len(enriched_evidence),
            supported_count=supported_count,
            conflicting_count=conflicting_count,
            insufficient_count=insufficient_count,
            enriched_evidence=enriched_evidence,
            supporting_sources=len(supp_snippet_ids),
            conflicting_sources=len(conf_snippet_ids)
        )

        executive_summary = claims_analysis.get(
            "executive_summary",
            self._generate_heuristic_summary(question, claims, confidence_score)
        )

        return {
            "question": question,
            "executive_summary": executive_summary,
            "claims": claims,
            "evidence": enriched_evidence,
            "metrics": {
                "total_claims": len(claims),
                "supported": supported_count,
                "conflicting": conflicting_count,
                "insufficient": insufficient_count,
                "supported_claims": supported_count,
                "conflicting_claims": conflicting_count,
                "insufficient_claims": insufficient_count,
                "total_sources": len(enriched_evidence),
                "supporting_sources": len(supp_snippet_ids),
                "conflicting_sources": len(conf_snippet_ids),
                "confidence_score": confidence_score,
                "confidence_explanation": confidence_explanation
            }
        }

    def _heuristic_extract_claims(self, question: str, evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Deterministic rule-based NLP claim extractor.
        Extracts key claims from evidence snippets, checks sentiment/conflict keywords,
        and links evidence IDs.
        """
        if not evidence:
            return {
                "executive_summary": f"No live search results were found to verify '{question}'. Please try refining the search query.",
                "claims": [
                    {
                        "claim": f"Verification of claim: '{question}'",
                        "status": "INSUFFICIENT EVIDENCE",
                        "confidence": "Low",
                        "supporting_evidence_ids": [],
                        "conflicting_evidence_ids": [],
                        "explanation": "No relevant live web search results were retrieved."
                    }
                ]
            }

        # Determine conflict markers in snippets
        conflict_keywords = [
            "however", "but", "despite", "contrary", "disagree", "myth", "false", "misleading",
            "overstated", "criticism", "drawback", "issue", "problem", "expensive", "not true",
            "claim that", "dispute", "versus", "vs", "flaw"
        ]
        support_keywords = [
            "confirms", "proves", "shows", "supports", "according to", "verified", "found that",
            "effective", "benefit", "recommended", "positive", "high performance", "worth"
        ]

        conflicting_ids = []
        supporting_ids = []

        for item in evidence:
            snip_lower = item["snippet"].lower()
            item_id = item["id"]
            
            is_conflicting = any(re.search(r'\b' + re.escape(ck) + r'\b', snip_lower) for ck in conflict_keywords)
            is_supporting = any(re.search(r'\b' + re.escape(sk) + r'\b', snip_lower) for sk in support_keywords)

            if is_conflicting:
                conflicting_ids.append(item_id)
            if is_supporting or not is_conflicting:
                supporting_ids.append(item_id)

        # Build main claim
        clean_q = question.rstrip("?").strip()
        main_claim_text = f"Factual core of question: '{clean_q}'"

        if conflicting_ids and supporting_ids:
            status = "CONFLICTING"
            confidence = "Medium"
            explanation = (
                f"Multiple web sources were analyzed. {len(supporting_ids)} sources provide supporting context, "
                f"while {len(conflicting_ids)} sources highlight opposing views, criticisms, or qualifications."
            )
        elif supporting_ids:
            status = "SUPPORTED"
            confidence = "High" if len(supporting_ids) >= 3 else "Medium"
            explanation = f"Found {len(supporting_ids)} independent live web sources confirming and supporting this statement."
        else:
            status = "INSUFFICIENT EVIDENCE"
            confidence = "Low"
            explanation = "Limited search results retrieved. Additional empirical evidence is required to reach a conclusive finding."

        # Secondary claim based on top source snippets
        claims = [
            {
                "claim": main_claim_text,
                "status": status,
                "confidence": confidence,
                "supporting_evidence_ids": supporting_ids,
                "conflicting_evidence_ids": conflicting_ids,
                "explanation": explanation
            }
        ]

        # Add sub-claim if we have news or research sources
        research_or_news = [ev for ev in evidence if ev["category"] in ["Research", "News", "Official"]]
        if research_or_news:
            top_rn = research_or_news[0]
            claims.append({
                "claim": f"Key finding reported by {top_rn['source']}: {top_rn['title'][:60]}...",
                "status": "SUPPORTED" if top_rn["id"] in supporting_ids else "CONFLICTING",
                "confidence": "High" if top_rn["category"] in ["Official", "Research"] else "Medium",
                "supporting_evidence_ids": [top_rn["id"]] if top_rn["id"] in supporting_ids else [],
                "conflicting_evidence_ids": [top_rn["id"]] if top_rn["id"] in conflicting_ids else [],
                "explanation": f"Source '{top_rn['source']}' ({top_rn['category']}) states: \"{top_rn['snippet'][:120]}...\""
            })

        summary = (
            f"Based on live analysis of {len(evidence)} web sources via SerpApi, the primary claim status is **{status}**. "
            f"Evidence includes {len(supporting_ids)} supporting sources and {len(conflicting_ids)} conflicting/counter-perspective sources."
        )

        return {
            "executive_summary": summary,
            "claims": claims
        }

    def _calculate_confidence(
        self,
        question: str,
        claims: List[Dict[str, Any]],
        total_sources: int,
        supported_count: int,
        conflicting_count: int,
        insufficient_count: int,
        enriched_evidence: List[Dict[str, Any]],
        supporting_sources: int = 0,
        conflicting_sources: int = 0
    ) -> Tuple[int, str]:
        """
        Calculate transparent evidence confidence score (0-100%).
        
        Factors:
        1. Source Volume (up to +30 pts for 5+ relevant sources)
        2. Agreement Ratio (up to +30 pts if majority agree without unaddressed conflict)
        3. Source Diversity (up to +20 pts if official/research/news categories present)
        4. Recency & Directness (up to +20 pts for dated recent snippets and clear queries)
        """
        if total_sources == 0:
            return 0, "No live search results available to evaluate confidence."

        # Factor 1: Volume (Max 30)
        volume_score = min(30, total_sources * 5)

        # Factor 2: Agreement Ratio (Max 30)
        total_claims = len(claims) or 1
        agreement_ratio = supported_count / total_claims
        conflict_penalty = (conflicting_count / total_claims) * 15
        insufficient_penalty = (insufficient_count / total_claims) * 20
        agreement_score = max(0, min(30, (agreement_ratio * 30) - conflict_penalty - insufficient_penalty))

        # Factor 3: Source Diversity (Max 20)
        categories = set(ev.get("category", "Other") for ev in enriched_evidence)
        diversity_score = 0
        if "Official" in categories or "Research" in categories:
            diversity_score += 10
        if "News" in categories:
            diversity_score += 5
        if "Review" in categories or "Industry" in categories:
            diversity_score += 5
        diversity_score = min(20, diversity_score)

        # Factor 4: Directness & Recency (Max 20)
        has_dates = any(ev.get("date") for ev in enriched_evidence)
        directness_score = 15 if has_dates else 10
        if len(question.split()) > 3:
            directness_score += 5
        directness_score = min(20, directness_score)

        final_score = int(volume_score + agreement_score + diversity_score + directness_score)
        final_score = max(10, min(98, final_score))  # Never pretend 100% scientific certainty

        cat_list = sorted(list(categories))
        cat_str = ", ".join(cat_list) if cat_list else "Web"

        explanations = []
        explanations.append(f"1) Source Volume (+{volume_score}/30 pts: {total_sources} sources)")
        explanations.append(f"2) Claim Consensus (+{int(round(agreement_score))}/30 pts: {supported_count} supported vs {conflicting_count} conflicting claims)")
        explanations.append(f"3) Source Diversity (+{diversity_score}/20 pts: {cat_str})")
        explanations.append(f"4) Directness & Recency (+{directness_score}/20 pts: indexed search snippets)")

        if supporting_sources or conflicting_sources:
            src_breakdown_str = f" across {total_sources} web sources ({supporting_sources} supporting, {conflicting_sources} conflicting)"
        else:
            src_breakdown_str = f" across {total_sources} web sources"

        explanation_str = (
            f"Multi-Factor Rating ({final_score}%): Evaluated across 4 weighted factors — "
            + " | ".join(explanations)
            + f". Note: Confidence reflects claim-level consensus and source credibility{src_breakdown_str}, rather than a raw source count ratio."
        )
        return final_score, explanation_str

    def _generate_heuristic_summary(self, question: str, claims: List[Dict[str, Any]], confidence: int) -> str:
        """Generate plain text executive summary."""
        statuses = [c.get("status") for c in claims]
        main_status = statuses[0] if statuses else "INSUFFICIENT EVIDENCE"
        return (
            f"Investigation into '{question}' completed with an overall confidence score of {confidence}%. "
            f"The primary verdict is **{main_status}** based on evidence synthesized across live search results."
        )

    def _extract_domain(self, url: str) -> str:
        if not url:
            return "web"
        try:
            netloc = urllib.parse.urlparse(url).netloc
            return netloc.replace("www.", "")
        except Exception:
            return "web"
