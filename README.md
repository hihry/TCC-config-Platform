# TCC Config Platform

**Chatbot for Tracking Content Configuration Management**

The TCC Config Platform is an AI-agentic, GitOps-governed configuration management system. It replaces a fragile, spreadsheet-driven workflow with a conversational chatbot that lets Product Managers author tracking content in natural language. The system guarantees referential integrity, schema validation, and provides a full audit trail via GitHub Pull Requests, all while leaving the highly-performant, deterministic downstream runtime untouched.

## 🚀 Key Features

* **Natural Language Authoring:** Use a chatbot interface to propose changes to tracking configurations.
* **Agentic State Machine:** Powered by LangGraph, requests move deterministically through `Planner` -> `Editor` -> `QA` -> `GitOps` nodes. Unvalidated changes can never reach Git.
* **In-Memory Data Engine:** Uses DuckDB to query configuration JSON files via SQL, avoiding large context window overhead.
* **Semantic Search Resolution:** Utilizes `all-MiniLM-L6-v2` embeddings to accurately map ambiguous user intents to exact localization keys.
* **Zero Runtime Impact:** Changes are authored in modular, hierarchical JSON but compiled back to flat, legacy schema format via CI/CD, requiring zero downstream engineering changes.

## 🏗️ Architecture

The platform is designed as a single stateless container composed of four main layers:

1. **Presentation Tier:** Streamlit UI (`app.py`)
2. **Agent Orchestration:** LangGraph state machine (`tcc_platform/graph.py`)
3. **Data Engine & Tooling:** DuckDB and SentenceTransformers (`tools/`)
4. **Persistence:** GitHub GitOps

## 📁 Directory Structure

```text
tcc-config-platform/
├── app.py                      # Streamlit Chat UI (Entry Point)
├── requirements.txt            # Python dependencies
├── repo/                       # Mocked data repository
│   ├── programs/               # Modular JSON configuration files
│   ├── KEY_*.csv               # Master localization dictionaries
│   └── compiled_main.json      # Flattened output for downstream tracking runtime
├── scripts/                    # Utilities and CI/CD tools
│   ├── generate_mock_data.py   # Generates sample legacy CSVs and dictionaries
│   ├── migrate_main.py         # Converts flat CSV to hierarchical JSON
│   ├── compile_for_trkxp.py    # Flattens JSON back to flat format for downstream APIs
│   └── validate_migration.py   # Validates JSON schema integrity
├── tcc_platform/               # AI Orchestration and LangGraph setup
│   ├── graph.py                # LangGraph state machine wiring
│   ├── state.py                # Graph state definitions
│   └── agents/                 # LLM and deterministic nodes
│       ├── planner.py          # Intent classification & SQL generation
│       ├── editor.py           # Patch proposal & semantic search
│       ├── qa.py               # Key validation (deterministic)
│       └── gitops.py           # Local patch application & PR creation
└── tools/                      # Deterministic Python tools for agents
    ├── db_retrieval.py         # DuckDB SQL execution layer
    ├── json_editor.py          # Safely applies patches to JSON
    └── localization_editor.py  # Dictionary loading, key validation, and semantic search
```

## 🛠️ Setup & Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   The application uses Google's Gemini models for the agent pipeline. Ensure your API key is set:
   ```bash
   # On Windows
   set GOOGLE_API_KEY=your_api_key_here
   # Or using PowerShell
   $env:GOOGLE_API_KEY="your_api_key_here"
   ```

3. **Initialize Mock Data**
   Generate the legacy spreadsheets, migrate them to JSON, and compile them to verify the pipeline:
   ```bash
   python scripts/generate_mock_data.py
   python scripts/migrate_main.py
   python scripts/compile_for_trkxp.py
   ```

## 💻 Usage

To launch the Product Manager chatbot interface:

```bash
streamlit run app.py
```

Try asking the chatbot to make a configuration change, for example:
> *"Change the message for standard inbound leg1 exceptions to say there is a weather delay."*

The chatbot will identify the target rule, run semantic search to find the correct alert/message key, validate the key through the QA node, and mock a GitHub Pull Request with the proposed change.
