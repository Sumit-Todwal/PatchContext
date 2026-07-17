from langchain_groq import ChatGroq
from dotenv import load_dotenv

from config import (
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)

load_dotenv()


def get_llm():
    """
    Create and return the Groq LLM.
    """

    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    return llm