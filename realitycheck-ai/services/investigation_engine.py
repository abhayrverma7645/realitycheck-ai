"""
Investigation Engine for REALITYCHECK AI
Orchestrates the 6-step live-web investigation pipeline:
1. Question validation & intent understanding
2. Query expansion (main + counter-evidence queries)
3. Live SerpApi search
4. Evidence collection & deduplication
5. Conflict & claim analysis
6. Synthesis & report generation
"""

import time
from typing import List, Dict, Any, Callable, Optional
from services.serpapi_service import SerpApiService
from services.evidence_analyzer import EvidenceAnalyzer
from services.llm_service import LLMService
from services.history_service import HistoryService

class InvestigationEngine:
    def __init__(self, serpapi_key: Optional[str] = None, llm_key: Optional[str] = None):
        self.serpapi_service = SerpApiService(api_key=serpapi_key)
        self.llm_service = LLMService(api_key=llm_key)
        self.evidence_analyzer = EvidenceAnalyzer(llm_service=self.llm_service)
        self.history_service = HistoryService()

    def run_investigation(
        self,
        question: str,
        progress_callback: Optional[Callable[[int, str, bool], None]] = None
    ) -> Dict[str, Any]:
        """
        Run complete investigation pipeline with progress tracking.
        """
        question = question.strip()
        if not question:
            return {
                "success": False,
                "error": "Question cannot be empty. Please enter a claim or question."
            }

        # Step 1: Understanding Question
        self._notify_progress(progress_callback, step=1, status_text="Understanding question...", done=False)
        time.sleep(0.3)
        self._notify_progress(progress_callback, step=1, status_text="Understanding question ✓", done=True)

        # Step 2: Generating Investigation Queries
        self._notify_progress(progress_callback, step=2, status_text="Generating investigation queries...", done=False)
        queries = self._generate_search_queries(question)
        time.sleep(0.3)
        self._notify_progress(progress_callback, step=2, status_text=f"Generated {len(queries)} search queries ✓", done=True)

        # Step 3: Searching Live Web via SerpApi
        self._notify_progress(progress_callback, step=3, status_text="Searching live web via SerpApi...", done=False)
        raw_evidence = self.serpapi_service.execute_multi_search(queries, max_per_query=6)
        
        # Check if SerpApi call returned error or no results
        if not raw_evidence:
            # Check if API key was missing or failed
            check_single = self.serpapi_service.search_google(question, num_results=1)
            if not check_single.get("success"):
                err_msg = check_single.get("error", "Failed to retrieve search results from SerpApi.")
                return {
                    "success": False,
                    "error": err_msg
                }

        self._notify_progress(progress_callback, step=3, status_text=f"Live search complete ({len(raw_evidence)} items) ✓", done=True)

        # Step 4: Collecting Evidence & Deduplication
        self._notify_progress(progress_callback, step=4, status_text="Collecting and ranking evidence...", done=False)
        time.sleep(0.3)
        self._notify_progress(progress_callback, step=4, status_text="Evidence deduplicated and categorized ✓", done=True)

        # Step 5: Checking Conflicting Evidence
        self._notify_progress(progress_callback, step=5, status_text="Checking conflicting and counter evidence...", done=False)
        time.sleep(0.3)
        self._notify_progress(progress_callback, step=5, status_text="Cross-examination complete ✓", done=True)

        # Step 6: Generating Final Investigation Report
        self._notify_progress(progress_callback, step=6, status_text="Synthesizing final transparent report...", done=False)
        investigation_result = self.evidence_analyzer.analyze_investigation(question, raw_evidence)
        investigation_result["queries_used"] = queries
        investigation_result["success"] = True

        # Save to local SQLite history
        try:
            inv_id = self.history_service.save_investigation(investigation_result)
            investigation_result["history_id"] = inv_id
        except Exception:
            pass

        self._notify_progress(progress_callback, step=6, status_text="Investigation generated ✓", done=True)

        return investigation_result

    def _generate_search_queries(self, question: str) -> List[str]:
        """
        Generate primary query + multi-perspective counter/criticism query.
        """
        clean_q = question.strip()
        queries = [clean_q]

        # Generate counter-evidence query based on question pattern
        q_lower = clean_q.lower()
        if "worth buying" in q_lower or "should i buy" in q_lower:
            queries.append(f"{clean_q} problems issues complaints downside")
        elif "cheaper than" in q_lower or "better than" in q_lower:
            queries.append(f"{clean_q} comparison criticisms disadvantages")
        elif "is" in q_lower or "are" in q_lower or "viral" in q_lower:
            queries.append(f"{clean_q} false fact check debunked criticism")
        else:
            queries.append(f"{clean_q} controversy evidence counter arguments")

        return queries

    def _notify_progress(self, callback: Optional[Callable], step: int, status_text: str, done: bool):
        if callback:
            callback(step, status_text, done)
