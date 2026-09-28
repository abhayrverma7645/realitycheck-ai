# REALITYCHECK AI 🔍
> **"Search the live web. Compare the evidence. Understand the claim."**

Submission for the **SerpApi Hackathon 2026**

---

## 🎯 Problem Statement
Traditional search engines return millions of blue links. When users need to verify a complex claim, make a purchase decision, or fact-check news, they must open dozens of tabs, struggle to reconcile conflicting articles, and guess which sources are credible. 

Search engines give you raw results. They do **not** synthesize evidence, surface contradictions, or evaluate claim-level confidence.

---

## 💡 Solution
**REALITYCHECK AI** turns raw live-web search results into an end-to-end fact investigation engine.

By placing **SerpApi** at its core, RealityCheck:
1. Deconstructs any complex question or claim into target sub-claims.
2. Formulates multi-perspective search queries (including counter-evidence and criticism queries).
3. Queries Google Search in real-time via SerpApi.
4. Categorizes sources into *Official, Research, News, Review, Industry, Community*.
5. Explicitly separates **Supporting Evidence** vs. **Conflicting Evidence** side-by-side.
6. Calculates a transparent, multi-factor confidence rating.
7. Visualizes claim relationships with an interactive Plotly network graph.
8. Generates publication-grade downloadable PDF investigation reports.

---

## 🏗️ Architecture & Pipeline

```
USER QUESTION / CLAIM
       │
       ▼
INVESTIGATION ENGINE ────► Query Expansion (Main + Counter Queries)
       │
       ▼
SERPAPI LIVE SEARCH  ────► Google Search SDK (Organic Web Results)
       │
       ▼
EVIDENCE EXTRACTOR   ────► Domain & Source Categorization
       │
       ▼
CLAIM & CONFLICT DETECTOR ──► Side-by-side Supporting vs. Conflicting Snippets
       │
       ▼
CONFIDENCE EVALUATOR ────► Multi-factor transparent scoring (0-100%)
       │
       ▼
TRANSPARENT REPORT   ────► Interactive UI, Plotly Graph, PDF Export
```

---

## 🛠️ Technology Stack
- **Core Platform:** Python 3.13+
- **Frontend / UI:** Streamlit (Custom SaaS theme, Glassmorphic CSS)
- **Live Web Search:** SerpApi Official Python SDK (`google-search-results`)
- **Data Visualization:** Plotly (Interactive Scatter Network Graph)
- **Data Handling:** pandas
- **PDF Report Engine:** ReportLab
- **Persistence:** Local SQLite database (`data/history.sqlite`)
- **Analysis Engine:** Rule-Based NLP Claim & Evidence Analyzer (with optional OpenAI LLM integration)
- **Testing:** Pytest & Python `unittest`

---

## ⚙️ Installation & Setup

Download or clone the project repository, then open the project folder in a terminal.

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Environment Variables Configuration
Copy `.env.example` to create your `.env` file:
```bash
cp .env.example .env
```
Edit `.env` and set your SerpApi key:
```env
SERPAPI_KEY=your_actual_serpapi_key_here
LLM_API_KEY=your_optional_llm_key_here
```

*Note: You can also enter or update API keys directly within the application's Sidebar UI at runtime.*

---

## 🚀 Running Locally

Launch the Streamlit app:
```bash
python -m streamlit run app.py
```
Open your browser at `http://localhost:8502`.

---

## 🧪 Running Unit Tests

Run the comprehensive unit test suite:
```bash
python -m pytest tests/
```

---

## 📖 Example Investigations
- *"Is this laptop worth buying in 2026?"*
- *"Are electric vehicles cheaper to own than petrol cars?"*
- *"What are the current software engineering career opportunities?"*
- *"Is this viral claim supported by reliable sources?"*

---

## 📄 Hackathon Presentation
See `DEMO_SCRIPT.md` for the 2–3 minute presentation script.

---

## 📜 License & Transparency Statement
RealityCheck AI does **not** hardcode fake search results, fabricate URLs, or hide contradictory evidence. All investigations perform live Google Search queries via SerpApi.

