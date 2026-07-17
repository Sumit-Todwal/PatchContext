from langchain_huggingface import HuggingFaceEmbeddings

from utils.logger import logger
from config import EMBEDDING_MODEL, EMBEDDING_DEVICE


def get_embedding_model():
    """
    Load and return the embedding model.
    """

    logger.info(
        f"Loading embedding model: {EMBEDDING_MODEL}"
    )

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": EMBEDDING_DEVICE
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    logger.info("Embedding model loaded successfully.")

    return embedding_model