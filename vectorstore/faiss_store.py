import os

from langchain_community.vectorstores import FAISS

from models.embedding_model import get_embedding_model

from utils.serialization import load_pickle
from utils.logger import logger

from config import (
    CHUNKS_FILE,
    FAISS_DIR,
    FAISS_INDEX_NAME
)


def load_chunks():
    """
    Load chunked LangChain Documents.
    """

    logger.info("Loading chunked documents...")

    chunks = load_pickle(CHUNKS_FILE)

    logger.info(
        f"Loaded {len(chunks)} chunks."
    )

    return chunks


def create_vectorstore(chunks):
    """
    Create a FAISS vector store from documents.
    """

    logger.info("Loading embedding model...")

    embedding_model = get_embedding_model()

    logger.info(
        "Generating embeddings and building FAISS index..."
    )

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    logger.info(
        f"Successfully indexed {len(chunks)} chunks."
    )

    return vectorstore


def save_vectorstore(vectorstore):
    """
    Save the FAISS vector store.
    """

    os.makedirs(
        FAISS_DIR,
        exist_ok=True
    )

    vectorstore.save_local(
        folder_path=FAISS_DIR,
        index_name=FAISS_INDEX_NAME
    )

    logger.info(
        "FAISS index saved successfully."
    )


def load_vectorstore():
    """
    Load an existing FAISS vector store.
    """

    logger.info(
        "Loading existing FAISS index..."
    )

    embedding_model = get_embedding_model()

    vectorstore = FAISS.load_local(
        folder_path=FAISS_DIR,
        embeddings=embedding_model,
        index_name=FAISS_INDEX_NAME,
        allow_dangerous_deserialization=True
    )

    logger.info(
        "FAISS index loaded successfully."
    )

    return vectorstore


def vectorstore_exists():
    """
    Check whether the FAISS index exists.
    """

    faiss_file = os.path.join(
        FAISS_DIR,
        f"{FAISS_INDEX_NAME}.faiss"
    )

    pickle_file = os.path.join(
        FAISS_DIR,
        f"{FAISS_INDEX_NAME}.pkl"
    )

    return (
        os.path.exists(faiss_file)
        and
        os.path.exists(pickle_file)
    )


def get_vectorstore():
    """
    Load the prebuilt FAISS vector store.
    """

    if not vectorstore_exists():
        raise FileNotFoundError(
            "FAISS index not found. Build it locally using "
            "'python vectorstore/faiss_store.py' before deployment."
        )

    return load_vectorstore()

def main():

    vectorstore = get_vectorstore()

    logger.info("=" * 60)
    logger.info("FAISS Statistics")
    logger.info("=" * 60)
    logger.info(
        f"Indexed Documents : {vectorstore.index.ntotal}"
    )
    logger.info(
        f"Embedding Model   : {get_embedding_model().model_name}"
    )
    logger.info("=" * 60)

    logger.info(
        "Vector store pipeline completed successfully."
    )


if __name__ == "__main__":
    main()