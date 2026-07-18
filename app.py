import streamlit as st
from chains.rag_chain import generate_answer

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="PatchContext",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown(
    """
    <style>
        .main-title{
            font-size:42px;
            font-weight:700;
        }

        .subtitle{
            color:gray;
            margin-bottom:25px;
        }

        .answer-box{
            background:#f6f8fa;
            padding:20px;
            border-radius:10px;
            border:1px solid #dddddd;
        }

        .footer{
            text-align:center;
            color:gray;
            font-size:14px;
            margin-top:40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:

    st.title("🧠 PatchContext")

    st.markdown(
        """
AI-powered GitHub Repository Assistant.

---

### 📌 Repository

Currently indexed:

🔗 **[FastAPI](https://github.com/fastapi/fastapi)**

Repository:
https://github.com/fastapi/fastapi

---

### ✨ Features

- GitHub Issues
- Pull Requests
- Commits
- Semantic Search
- FAISS Vector Store
- Groq LLM
- Source Attribution

---

### 💡 Example Questions

- How does dependency injection work?

- Explain background tasks.

- Which PR added lifespan support?

- How is authentication implemented?

- Explain WebSocket support.

---

Version **1.0**
"""
    )

# -------------------------------
# Header
# -------------------------------
st.markdown(
    "<div class='main-title'>🧠 PatchContext</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='subtitle'>Ask questions about the FastAPI GitHub repository using Retrieval-Augmented Generation.</div>",
    unsafe_allow_html=True,
)

st.markdown("""
<style>
div[data-testid="InputInstructions"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Question Input
# -------------------------------
question = st.text_area(
    "Ask a Question",
    placeholder="Example: How does dependency injection work?",
    height=150,
)

ask = st.button(
    "🚀 Ask PatchContext",
    use_container_width=True,
)

# -------------------------------
# Generate Answer
# -------------------------------
if ask:

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Searching repository and generating answer..."):

                result = generate_answer(question)

            st.success("Answer generated successfully!")

            st.divider()

            st.subheader("📖 Answer")

            with st.container(border=True):

                st.markdown(result["answer"])

            st.divider()

            st.subheader("🔗 Sources")

            if result["sources"]:

                for source in result["sources"]:

                    label = source.get("label", "Unknown")

                    url = source.get("url", "")

                    if url:
                        st.markdown(f"✅ [{label}]({url})")

                    else:
                        st.markdown(f"✅ {label}")

            else:

                st.info("No sources available.")

        except Exception as e:

            st.error("Something went wrong while generating the answer.")

            with st.expander("Error Details"):
                st.code(str(e))

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")

st.markdown(
    """
<div class='footer'>
PatchContext • Retrieval-Augmented Generation for GitHub Repositories
</div>
""",
    unsafe_allow_html=True,
)