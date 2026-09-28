# REALITYCHECK AI - JUDGE PITCH & PRESENTATION GUIDE (`JUDGE_PITCH.md`)

> **Tagline:** *"Search the live web. Compare the evidence. Understand the claim."*

---

## ⚡ 1. 20-Second Elevator Pitch
"Search engines give you a wall of 10 blue links and force you to open 15 tabs to compare conflicting articles. **RealityCheck AI** uses SerpApi to query the live web, extract core claims, isolate supporting versus conflicting evidence side-by-side, and deliver an interactive, source-backed investigation report in seconds."

---

## ⏱️ 2. 60-Second Product Explanation
"When people make major purchasing decisions, verify breaking news, or fact-check viral claims, traditional search engines fail them. They return isolated links without context or conflict detection.

**RealityCheck AI** transforms web search into an automated investigation:
1. It takes any user query and expands it into multi-perspective search queries.
2. It fetches real-time Google Search results via **SerpApi**.
3. It categorizes sources into *Official, Research, News, Review,* and *Community*.
4. It isolates **Supporting Evidence** alongside **Conflicting Evidence** side-by-side so users see the full truth.
5. It visualizes claim relationships in an interactive Plotly network graph and exports publication-ready PDF reports.

Search engines give you results. RealityCheck turns those results into an investigation."

---

## 🎙️ 3. Complete 2–3 Minute Pitch

### The Problem
Every day, millions of people turn to Google to answer complex questions: *"Are electric vehicles actually cheaper to maintain?"*, *"Is this viral health claim true?"*, *"Is this laptop worth buying in 2026?"*

Current search engines return pages of search results, ads, and SEO-optimized blogs. Users are left to manually open dozens of browser tabs, cross-examine conflicting statistics, filter out bias, and guess which sources are trustworthy. Search engines do not synthesize evidence or highlight contradictions.

### The Solution
**RealityCheck AI** is an AI-powered live-web investigation platform that automates the entire fact-checking process. Instead of returning raw links, RealityCheck deconstructs questions into factual sub-claims, queries the live web via SerpApi, categorizes source domains, surfaces conflicting evidence side-by-side, calculates a transparent confidence score, and generates interactive graphs and PDF reports.

### Why SerpApi is Essential
SerpApi is the core data pipeline engine of RealityCheck AI. Live web investigations require real-time, structured access to Google Search organic results, top news, and answer boxes. SerpApi enables multi-query expansion—running primary queries alongside counter-evidence queries seamlessly—without rate-limit bottlenecks or complex scraping overhead. Without SerpApi, real-time live web evidence synthesis would not be possible.

### What Makes RealityCheck Different
1. **Conflict Detection:** We don't hide disagreement or pretend there's 100% consensus when sources conflict. We show supporting evidence on the left and conflicting evidence on the right.
2. **Transparent Confidence:** Confidence scores (0–100%) are calculated mathematically from source volume, agreement ratios, source diversity, and recency—without scientific pretense.
3. **No Hallucinations:** Every claim and evidence snippet is tied directly to real-time Google Search results with clickable source links.
4. **Interactive Network Graph:** Plotly-powered hierarchical tree mapping Question → Claims → Evidence → Sources.

---

## 🏗️ 4. Technical Architecture

```
USER QUESTION / CLAIM
       │
       ▼
INVESTIGATION ENGINE ────► Query Expansion (Primary + Counter Queries)
       │
       ▼
SERPAPI LIVE SEARCH  ────► Google Search SDK (Organic, News, Answer Boxes)
       │
       ▼
EVIDENCE EXTRACTOR   ────► Domain Categorization (Official, Research, News)
       │
       ▼
CLAIM & CONFLICT DETECTOR ──► Side-by-side Supporting vs. Conflicting Snippets
       │
       ▼
CONFIDENCE EVALUATOR ────► Multi-factor scoring (Volume + Agreement + Diversity)
       │
       ▼
TRANSPARENT REPORT   ────► Streamlit UI, Plotly Graph, ReportLab PDF Export
```

---

## 🚀 5. Future Potential
1. **Multi-Engine SerpApi Integration:** Expand beyond Google Search to include SerpApi Bing, Google Scholar, YouTube transcripts, and Google News APIs.
2. **Automated Citation API:** Provide an embeddable REST API for media organizations and research institutions to run live evidence audits.
3. **Browser Extension:** A real-time browser plugin that automatically runs RealityCheck investigations on news articles as users read them.
