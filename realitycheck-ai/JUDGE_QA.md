# REALITYCHECK AI - HACKATHON JUDGE Q&A GUIDE (`JUDGE_QA.md`)

This guide provides concise, technically accurate answers to questions likely to be asked by hackathon judges.

---

### Q1: Why SerpApi? Why not scrape web pages directly or use standard search APIs?
**Answer:**  
"SerpApi is the backbone of RealityCheck AI because live evidence investigations require structured, real-time access to Google Search's ecosystem—including organic results, top news, and answer boxes. Scraping directly is unreliable, fragile to layout changes, and prone to IP blocks. SerpApi gives us a clean, fast Python SDK that supports multi-query execution (querying both supporting and counter-evidence queries simultaneously) with enterprise-grade reliability."

---

### Q2: What exact problem does RealityCheck AI solve?
**Answer:**  
"Search engines give you 10 blue links; they don't give you synthesized evidence. When a user asks a complex question like *'Are EVs cheaper to maintain than petrol cars?'*, they are forced to open 15 tabs and reconcile conflicting statements manually. RealityCheck automates this by extracting factual sub-claims, isolating supporting versus conflicting evidence side-by-side, and calculating a transparent confidence score."

---

### Q3: How does evidence analysis work behind the scenes?
**Answer:**  
"Our pipeline follows a 6-step flow:
1. **Query Expansion:** We formulate the user's question into a primary search query plus counter-evidence queries (e.g. `[query] criticisms counter arguments false`).
2. **SerpApi Live Search:** We query Google Search via SerpApi.
3. **Source Categorization:** We classify domains into *Official (.gov/.edu), Research, News, Review, Industry,* and *Community*.
4. **Claim Detection:** We extract key factual sub-claims.
5. **Conflict Alignment:** Snippets are analyzed for support versus contradiction markers.
6. **Synthesis:** We build interactive Plotly graphs, metrics dashboards, and exportable PDFs."

---

### Q4: How do you detect conflicting evidence without bias?
**Answer:**  
"We explicitly search for counter-evidence by generating counter-perspective queries via SerpApi (e.g. `[claim] problems issues complaints counter arguments`). We then analyze search snippets for conflict markers (e.g., *however, despite, contrary, drawback, problem, expensive, misleading*). If sources provide opposing data, both supporting and conflicting evidence cards are displayed side-by-side. We never obscure disagreement."

---

### Q5: How is the confidence score calculated? Is it just a random number?
**Answer:**  
"No, the confidence score (0–100%) is calculated mathematically based on four weighted factors:
1. **Source Volume (30%):** Total number of relevant live search results.
2. **Agreement Ratio (30%):** Proportion of claims supported versus conflicting or unverified.
3. **Source Diversity (20%):** Presence of high-authority domain categories (Official .gov/.edu, peer-reviewed research, reputable news).
4. **Recency & Directness (20%):** Snippet recency and query alignment.
We deliberately cap the maximum score at 98% to avoid presenting AI analysis with false scientific certainty."

---

### Q6: How do you prevent AI hallucinations and fake sources?
**Answer:**  
"RealityCheck AI **cannot** hallucinate sources because all evidence items are generated strictly from live SerpApi Google Search payloads. Every snippet displayed in our UI and PDF report contains an immutable `source`, `domain`, and direct clickable `[Open Source]` URL retrieved live from Google Search."

---

### Q7: What happens when sources disagree on a claim?
**Answer:**  
"When sources disagree, RealityCheck assigns the claim a status of `⚠️ CONFLICTING EVIDENCE`. Instead of forcing a single verdict, the UI renders a split two-column view showing **Green Supporting Evidence** on the left and **Red Conflicting Evidence** on the right, allowing the user to examine both perspectives."

---

### Q8: What happens if SerpApi fails or an API key is missing?
**Answer:**  
"Our application includes robust error boundary handling. If a SerpApi key is missing or invalid, the app catches the exception gracefully, displays a clean alert box explaining the missing configuration, and provides a runtime **🔑 API Key Settings** panel in the sidebar so judges can input a key on the fly without restarting the server."

---

### Q9: What technologies were used to build RealityCheck AI?
**Answer:**  
- **Python 3.14+** core backend
- **Streamlit** modern SaaS web UI
- **SerpApi SDK (`google-search-results`)** live Google Search pipeline
- **Plotly** interactive evidence network graphs
- **ReportLab** publication-grade PDF report engine
- **SQLite** local history persistence (`data/history.sqlite`)
- **Pytest** automated unit testing suite

---

### Q10: What would you improve with more time?
**Answer:**  
1. **Multi-Engine Expansion:** Integrate SerpApi Google Scholar and SerpApi YouTube transcript search for deeper academic and video evidence extraction.
2. **Real-Time Fact-Checking Browser Extension:** Build a Chrome extension that runs RealityCheck investigations automatically on news articles as users read them.
3. **Multi-Language Support:** Utilize SerpApi's `gl` and `hl` location/language parameters to cross-examine global news coverage in multiple languages.
