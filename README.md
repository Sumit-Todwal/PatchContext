# PatchContext

A Retrieval-Augmented Generation (RAG) system that answers design and implementation questions about the [FastAPI](https://github.com/fastapi/fastapi) GitHub repository, using its commits, pull requests, issues, and discussion comments as grounded, cited context.

Ask something like *"How does dependency injection work?"* or *"Which PR added lifespan support?"* and PatchContext retrieves the most relevant repository history and answers with source attribution back to the original commit, PR, or issue.

## How It Works

```
GitHub REST API
      │
      ▼
ingestion/           → fetches commits, pull requests, issues, and PR/issue comments
                        via the GitHub API (paginated, with retry + backoff)
      │
      ▼
preprocessing/        → normalizes each source type into a common document format,
                         removes empty/short/duplicate/dependency-bump noise,
                         and splits documents into overlapping chunks
                         (tiktoken-aware, 500 tokens / 100 overlap)
      │
      ▼
vectorstore/          → embeds chunks locally with BAAI/bge-small-en-v1.5
                         and builds a FAISS index
      │
      ▼
retrieval/            → retrieves relevant chunks using Maximal Marginal
                         Relevance (k=5, fetch_k=20, λ=0.5) for a mix of
                         relevance and diversity, then formats them with
                         metadata into an LLM-ready context block
      │
      ▼
chains/rag_chain.py   → prompts an LLM (Groq's llama-3.3-70b-versatile) with
                         the retrieved context and extracts a deduplicated
                         list of sources (Issue / PR / Commit / Comment)
      │
      ▼
app.py                 → Streamlit UI: ask a question, get an answer with
                          its sources linked
```

## Tech Stack

| Layer | Choice |
|---|---|
| Orchestration | LangChain |
| LLM | Groq — `llama-3.3-70b-versatile` |
| Embeddings | HuggingFace `BAAI/bge-small-en-v1.5` (local, CPU) |
| Vector store | FAISS |
| Retrieval strategy | Maximal Marginal Relevance (MMR) |
| Data source | GitHub REST API (commits, PRs, issues, comments) |
| UI | Streamlit |

## Project Structure

```
PatchContext/
├── app.py                # Streamlit UI
├── chains/rag_chain.py   # Retrieval + LLM call, source extraction
├── config/                # Central settings: target repo, models, chunking, paths
├── ingestion/              # GitHub API client + fetch scripts (commits, PRs, issues, comments)
├── preprocessing/          # Normalize, clean, and chunk raw data into embeddable documents
├── models/                 # LLM and embedding model factories
├── vectorstore/             # FAISS index build / load / save
├── retrieval/               # Retriever construction + context formatting
├── prompts/                 # RAG prompt template
└── requirements.txt
```

## Setup

**1. Clone and install**
```bash
git clone https://github.com/Sumit-Todwal/PatchContext.git
cd PatchContext
python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**2. Environment variables**

Create a `.env` file in the project root:
```
GITHUB_TOKEN=your_github_personal_access_token
GROQ_API_KEY=your_groq_api_key
```
`GITHUB_TOKEN` raises the GitHub API rate limit from 60 to 5,000 requests/hour — needed since ingestion is paginated.

**3. Set the target repository**

`config/github.py` needs `REPO_OWNER` and `REPO_NAME` defined:
```python
REPO_OWNER = "fastapi"
REPO_NAME = "fastapi"
```

**4. Run the pipeline once, in order**
```bash
python -m ingestion.fetch_commits
python -m ingestion.fetch_prs
python -m ingestion.fetch_issues
python -m ingestion.fetch_pr_comments
python -m ingestion.fetch_issues_comments
python -m preprocessing.document_builder
python -m preprocessing.cleaner
python -m preprocessing.chunker
python -m vectorstore.faiss_store
```
This builds `data/raw/`, `data/processed/`, and the FAISS index at `data/faiss/`. `DEVELOPMENT_MODE` in `config/settings.py` caps comment-fetching to the first 20 PRs/issues — raise `MAX_PRS_TO_PROCESS` / `MAX_ISSUES_TO_PROCESS` for a larger index.

**5. Run the app**
```bash
streamlit run app.py
```

## Deployment (Streamlit Community Cloud)

`data/` (including the FAISS index) is gitignored by default, so a fresh deployment needs it committed:

```bash
git add -f data/faiss/github_index.faiss data/faiss/github_index.pkl
git commit -m "Add prebuilt FAISS index for deployment"
git push
```

Then on **share.streamlit.io**:
1. **New app** → repo `Sumit-Todwal/PatchContext`, branch `main`, main file `app.py`
2. **Advanced settings → Secrets** →
   ```
   GROQ_API_KEY = "your_groq_api_key"
   ```
3. Deploy. The app loads the committed FAISS index directly — no ingestion runs on the server, and `GITHUB_TOKEN` isn't needed there since that's only used for the local build step above.

## Roadmap

- Hallucination guard: a check that flags answer sentences not clearly supported by the retrieved context.
- RAGAs-based evaluation of the pipeline (faithfulness, answer relevancy, context precision) against a fixed question set.