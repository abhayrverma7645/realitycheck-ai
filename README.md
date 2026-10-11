🔍 RealityCheck AI

Search the live web. Compare the evidence. Understand the claim.

RealityCheck AI is a web-based fact-investigation tool built with Python and Streamlit. It uses SerpApi to search the live web and helps users explore evidence related to claims, including potentially supporting and conflicting information.

🎯 Problem Statement

Finding information online is easy, but evaluating conflicting sources and understanding the evidence behind a claim can be difficult. RealityCheck AI aims to make this process more structured, transparent, and accessible.

✨ Key Features

- 🔎 Live Web Search: Retrieve web results using SerpApi.
- ⚖️ Evidence Analysis: Identify potentially supporting and conflicting evidence using the project's analysis logic.
- 📊 Claim Assessment: Present claim-level assessments and confidence indicators.
- 🌐 Source Exploration: Inspect evidence and the web sources behind it.
- 🕸️ Evidence Graph: Explore connections between claims, evidence, and sources.
- 🧪 Testing: Includes automated tests for important application behavior.

Note: Assessments are automated indicators to support investigation, not definitive proof that a claim is true or false.

🛠️ Technology Stack

- Python
- Streamlit
- SerpApi
- Pytest

### 📌 Final Version

The final implementation, with the LLM dependency removed, is located in `realitycheck-ai-FINAL/realitycheck-ai/`.

Please use this folder when reviewing or running the final version. The separate `realitycheck-ai/` folder contains an earlier version of the project.


🏗️ Project Structure

realitycheck-ai/
├── app.py
├── config.py
├── components/
├── services/
├── data/
├── tests/
├── requirements.txt
├── README.md
├── DEMO_RUN.md
├── DEMO_SCRIPT.md
├── JUDGE_PITCH.md
└── JUDGE_QA.md

🚀 Getting Started

1. Clone the repository

git clone https://github.com/abhayrverma7645/realitycheck-ai.git
cd realitycheck-ai/realitycheck-ai

2. Install dependencies

Create a virtual environment if desired, then install the project dependencies:

py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt

On macOS or Linux, activate the environment with:

source .venv/bin/activate

3. Configure your API key

Obtain a SerpApi API key and configure it using the application's supported API-key settings or the environment-variable method documented in the project.

Security: Never commit your real API key, passwords, or other secrets to GitHub.

4. Run the application

py -m streamlit run app.py

If the "py" command is unavailable on your system, use the equivalent "python" command.

🧪 Run Tests

From the application directory, run:

py -m pytest tests/

📚 Documentation

- "DEMO_RUN.md" — instructions for running the demo
- "DEMO_SCRIPT.md" — demonstration script
- "JUDGE_PITCH.md" — project pitch
- "JUDGE_QA.md" — questions and answers for project presentation

🔐 Responsible Use

RealityCheck AI is an investigative aid, not a replacement for critical thinking or expert verification. Search results may be incomplete, outdated, or contradictory. Always inspect the original sources before making important decisions.

👨‍💻 Author

Abhay Verma

Developed as a project exploring live web search, evidence analysis, and transparent claim investigation.

📄 License

No license has been specified yet. Contact the repository owner for permission before reusing or redistributing this project.
