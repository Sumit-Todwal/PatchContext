from langchain_core.prompts import ChatPromptTemplate


CONTEXT_CHECK_PROMPT = ChatPromptTemplate.from_template(
    """
You are a relevance checker for a GitHub repository RAG system.

Determine whether the provided repository context contains
enough information to answer the user's question accurately.

Return ONLY one word:

YES

or

NO

Rules:
- Return YES only when the context contains enough evidence
  to answer the question.
- Return NO when the context is unrelated, insufficient,
  ambiguous, or missing the information required.
- Do not use your own knowledge.
- Do not explain your decision.

====================
Repository Context
====================

{context}

====================
Question
====================

{question}

====================
Decision
====================
"""
)