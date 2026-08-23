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

        .main-title {
            font-size: 42px;
            font-weight: 700;
        }

        .subtitle {
            color: gray;
            margin-bottom: 25px;
        }

        .footer {
            text-align: center;
            color: gray;
            font-size: 14px;
            margin-top: 40px;
        }

        /* Search status cards */
        .status-card {
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 8px;
            border: 1px solid rgba(128, 128, 128, 0.25);
        }

        .status-title {
            font-weight: 600;
            margin-bottom: 3px;
        }

        .status-description {
            color: #999999;
            font-size: 14px;
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
- Repository Context Search
- Web Search Fallback
- Source Attribution

---

### 💡 Example Questions

- How does dependency injection work?

- Explain background tasks.

- Which PR added lifespan support?

- How are responses serialized?

- Explain WebSocket support.

- What is the latest FastAPI version?

---

### 🔎 Search Strategy

PatchContext first searches the indexed repository.

If the repository context is insufficient,
web search is used as a fallback.

---

Version **2.0**
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
    "<div class='subtitle'>"
    "Ask questions about the FastAPI GitHub repository "
    "using Retrieval-Augmented Generation with web fallback."
    "</div>",
    unsafe_allow_html=True,
)


# -------------------------------
# Hide Input Instructions
# -------------------------------
st.markdown(
    """
    <style>
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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

            # ---------------------------------------
            # Generate answer
            # ---------------------------------------
            with st.spinner("🔎 Searching repository context..."):

                result = generate_answer(question)

            # ---------------------------------------
            # Read result safely
            # ---------------------------------------
            answer = result.get(
                "answer",
                "No answer was generated."
            )

            source_type = result.get(
                "source_type",
                "context"
            )

            context_found = result.get(
                "context_found",
                False
            )

            web_searched = result.get(
                "web_searched",
                False
            )

            context_sources = result.get(
                "context_sources",
                []
            )

            web_sources = result.get(
                "web_sources",
                []
            )

            # ---------------------------------------
            # Success message
            # ---------------------------------------
            st.success("Answer generated successfully!")

            st.divider()

            # =======================================
            # SEARCH PROCESS
            # =======================================

            st.subheader("🔎 Search Process")

            # ---------------------------------------
            # Context + Web status
            # ---------------------------------------

            if source_type == "context":

                col1, col2 = st.columns(2)

                with col1:

                    st.success(
                        "📚 Repository Context\n\n"
                        "Relevant information found."
                    )

                with col2:

                    st.info(
                        "🌐 Web Search\n\n"
                        "Not required."
                    )

            elif source_type == "web":

                col1, col2 = st.columns(2)

                with col1:

                    st.warning(
                        "📚 Repository Context\n\n"
                        "Context was insufficient."
                    )

                with col2:

                    st.success(
                        "🌐 Web Search\n\n"
                        "Additional information retrieved."
                    )

            elif source_type == "both":

                col1, col2 = st.columns(2)

                with col1:

                    st.success(
                        "📚 Repository Context\n\n"
                        "Used in the answer."
                    )

                with col2:

                    st.success(
                        "🌐 Web Search\n\n"
                        "Used for additional information."
                    )

            else:

                # Fallback if source_type is missing
                if context_found:

                    st.success(
                        "📚 Repository context was used."
                    )

                if web_searched:

                    st.info(
                        "🌐 Web search was used."
                    )

            # =======================================
            # ANSWER
            # =======================================

            st.divider()

            st.subheader("📖 Answer")

            with st.container(border=True):

                st.markdown(answer)

            # =======================================
            # REPOSITORY SOURCES
            # =======================================

            if context_sources:

                st.divider()

                st.subheader("📚 Repository Context")

                st.caption(
                    "Information retrieved from the indexed "
                    "FastAPI repository."
                )

                for source in context_sources:

                    label = source.get(
                        "label",
                        "Unknown source"
                    )

                    url = source.get(
                        "url",
                        ""
                    )

                    if url:

                        st.markdown(
                            f"📄 [{label}]({url})"
                        )

                    else:

                        st.markdown(
                            f"📄 {label}"
                        )

            # ---------------------------------------
            # No repository context
            # ---------------------------------------

            elif source_type == "web":

                st.divider()

                st.subheader("📚 Repository Context")

                st.caption(
                    "No sufficient repository information "
                    "was found for this question."
                )

            # =======================================
            # WEB SOURCES
            # =======================================

            # IMPORTANT:
            # Only display this section when web search
            # was actually used.

            if web_searched:

                st.divider()

                st.subheader("🌐 Web Search Results")

                st.caption(
                    "External sources retrieved because "
                    "repository context was insufficient."
                )

                if web_sources:

                    for source in web_sources:

                        label = source.get(
                            "label",
                            "Web source"
                        )

                        url = source.get(
                            "url",
                            ""
                        )

                        if url:

                            st.markdown(
                                f"🌐 [{label}]({url})"
                            )

                        else:

                            st.markdown(
                                f"🌐 {label}"
                            )

                else:

                    st.info(
                        "Web search was used, but no "
                        "source links were returned."
                    )

            # =======================================
            # SOURCE SUMMARY
            # =======================================

            st.divider()

            if source_type == "context":

                st.caption(
                    "📚 Answer generated from repository context."
                )

            elif source_type == "web":

                st.caption(
                    "🌐 Answer generated using web search "
                    "because repository context was insufficient."
                )

            elif source_type == "both":

                st.caption(
                    "📚🌐 Answer generated using both "
                    "repository context and web information."
                )

        except Exception as e:

            st.error(
                "Something went wrong while generating the answer."
            )

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