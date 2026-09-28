# REALITYCHECK AI - HACKATHON DEMO RUNBOOK (`DEMO_RUN.md`)

> **Tagline:** *"Search the live web. Compare the evidence. Understand the claim."*

---

## 🎯 Primary Demo Question
**`"Are electric vehicles cheaper to maintain than petrol cars?"`**

### Why This Question Was Selected:
1. **High Consumer Relevance:** Millions of consumers ask this question when evaluating vehicle purchases.
2. **Multi-Perspective Reality:** While EVs generally have fewer moving parts (supporting lower routine maintenance costs), significant counter-arguments and qualifications exist (high battery replacement costs, accelerated tire wear, and expensive insurance).
3. **Showcases Core Differentiator:** Plain search engines display 10 isolated links. RealityCheck AI synthesizes the evidence, isolates claims, and displays **Supporting Evidence** alongside **Conflicting Evidence** side-by-side.

---

## ⏱️ Step-by-Step Demo Sequence & Script

| Time | Screen / View | Action | Speaking Script |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:20** | **Main Screen: Header & Hero** | Point to title, tagline, and SerpApi transparency badge | *"Welcome to RealityCheck AI! Traditional search engines give you a wall of blue links. When you're making a big decision or fact-checking a claim, you're forced to open 15 tabs and compare conflicting statements manually. Search engines give you results; RealityCheck turns those results into an investigation."* |
| **0:20 - 0:45** | **Search Panel & Progress Tracker** | Type query (or click example button) & press **🚀 Investigate Claim** | *"Watch what happens when I enter 'Are electric vehicles cheaper to maintain than petrol cars?'. RealityCheck doesn't run just one search query. It understands the intent, generates counter-evidence queries via SerpApi, and queries the live web in real time."* |
| **0:45 - 1:15** | **Investigation Summary & Metrics** | Scroll to top summary tiles and confidence banner | *"In seconds, RealityCheck completes a 6-step investigation. Notice the summary dashboard: 2 claims evaluated across live web sources—1 claim is SUPPORTED, 1 has CONFLICTING EVIDENCE, with a transparent 57% confidence rating based on source volume and agreement."* |
| **1:15 - 1:45** | **Claims & Evidence Breakdown** | Open **⚖️ Claims & Evidence** tab; point to side-by-side cards | *"Here is our key innovation. On Claim #1, official sources like the U.S. Department of Energy confirm that routine maintenance costs 40% less. But on Claim #2, Consumer Reports highlights conflicting evidence about expensive battery replacements. Both perspectives are laid out side-by-side."* |
| **1:45 - 2:15** | **Interactive Evidence Graph** | Click **🕸️ Interactive Evidence Graph** tab | *"To make complex investigations intuitive, we built an interactive Plotly evidence graph. You can trace from the target question down to individual sub-claims, supporting green evidence nodes, and red conflicting evidence nodes."* |
| **2:15 - 2:35** | **Live Evidence Explorer** | Click **📚 Live Evidence Explorer** tab | *"Every single snippet is backed by live web data categorized into Official, Research, News, and Review sources, complete with direct clickable source hyperlinks."* |
| **2:35 - 3:00** | **PDF Report Export & Closing** | Click **📄 Download PDF Report** button | *"With one click, users can export a publication-ready PDF investigation report. RealityCheck transforms web search from passive browsing into transparent, evidence-backed decision making. Thank you!"* |

---

## 🔄 Backup Demo Question
**Backup Query:** `"Is this laptop worth buying in 2026?"`
- **Use Case:** Use if demoing consumer hardware purchasing or if testing a simpler product-oriented query.

---

## 🛠️ Failure Recovery Procedures

### Scenario A: Missing / Expired SerpApi Key
1. Open the **Sidebar Navigation**.
2. Expand **🔑 API Key Settings**.
3. Paste a fresh `SERPAPI_KEY` into the input field.
4. Click **🚀 Investigate Claim** again to resume live searching.

### Scenario B: Network Interruption / Slow Connection
1. If live network latency occurs during a presentation, navigate to **📜 Investigation History** in the sidebar.
2. Click **📂 Re-open** on any previously completed investigation to load pre-fetched live evidence instantly without calling external APIs.
