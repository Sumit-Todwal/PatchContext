import os
from openai import OpenAI
from dotenv import load_dotenv

from config import LLM_MODEL

load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def web_search(question: str) -> dict:
    """
    Search the web using Groq's built-in browser search.
    """

    response = client.responses.create(
        model=LLM_MODEL,
        input=f"""
You are a web research assistant for PatchContext.

Search the web for the following question:

{question}

Provide a concise, accurate answer based on the information
you find on the web.

Prefer authoritative and primary sources when possible.
Clearly distinguish current information from older information.
""",
        tools=[
            {
                "type": "browser_search"
            }
        ],
        tool_choice="required",
    )

    return {
        "answer": response.output_text,
        "raw_response": response,
    }