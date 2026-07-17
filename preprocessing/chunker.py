from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.file_utils import load_json
from utils.serialization import save_pickle
from utils.logger import logger

from config import (
    CLEAN_DOCUMENTS_FILE,
    CHUNKS_FILE,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL
)


def load_documents():
    """
    Load cleaned documents from disk.
    """
    logger.info("Loading cleaned documents...")

    documents = load_json(CLEAN_DOCUMENTS_FILE)

    logger.info(f"Loaded {len(documents)} cleaned documents.")

    return documents


def convert_to_langchain_documents(documents):
    """
    Convert normalized dictionaries into LangChain Document objects.
    """

    logger.info("Converting to LangChain Documents...")

    langchain_documents = []

    for document in documents:

        metadata = document["metadata"].copy()

        metadata["id"] = document["id"]
        metadata["type"] = document["type"]

        langchain_document = Document(
            page_content=document["text"],
            metadata=metadata
        )

        langchain_documents.append(langchain_document)

    logger.info(
        f"Converted {len(langchain_documents)} documents."
    )

    return langchain_documents


def split_documents(documents):
    """
    Split LangChain Documents into overlapping token-based chunks.
    """

    logger.info("Splitting documents...")

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name=EMBEDDING_MODEL,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    # Assign a unique ID to every chunk
    for index, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = (
            f"{chunk.metadata['id']}_chunk_{index}"
        )

    logger.info(
        f"Generated {len(chunks)} chunks."
    )

    return chunks


def print_statistics(documents, chunks):
    """
    Print chunking statistics.
    """

    logger.info("=" * 60)
    logger.info("Chunking Statistics")
    logger.info("=" * 60)

    logger.info(f"Documents          : {len(documents)}")
    logger.info(f"Chunks             : {len(chunks)}")

    if documents:
        logger.info(
            f"Chunks / Document  : {len(chunks) / len(documents):.2f}"
        )

    logger.info(f"Chunk Size         : {CHUNK_SIZE}")
    logger.info(f"Chunk Overlap      : {CHUNK_OVERLAP}")
    logger.info(f"Embedding Model    : {EMBEDDING_MODEL}")

    logger.info("=" * 60)


def inspect_chunks(chunks, num_samples=3):
    """
    Print a few sample chunks for manual inspection.
    """

    logger.info("=" * 80)
    logger.info("Sample Chunks")
    logger.info("=" * 80)

    for i, chunk in enumerate(chunks[:num_samples], start=1):

        logger.info(f"Chunk {i}")
        logger.info(f"Source : {chunk.metadata.get('type')}")
        logger.info(f"ID     : {chunk.metadata.get('id')}")
        logger.info(
            f"Chunk ID: {chunk.metadata.get('chunk_id')}"
            )
        
        logger.info(
            f"Length : {len(chunk.page_content)} characters"
        )

        logger.info("-" * 60)

        preview = (
            chunk.page_content[:400]
            .replace("\n", " ")
            .strip()
        )

        logger.info(preview)

        logger.info("=" * 80)


def save_chunks(chunks):
    """
    Save chunked LangChain Documents.
    """

    save_pickle(
        chunks,
        CHUNKS_FILE
    )


def main():

    documents = load_documents()

    langchain_documents = convert_to_langchain_documents(
        documents
    )

    chunks = split_documents(
        langchain_documents
    )

    print_statistics(
        langchain_documents,
        chunks
    )

    inspect_chunks(
        chunks
    )

    save_chunks(
        chunks
    )

    logger.info(
        "Chunking pipeline completed successfully."
    )


if __name__ == "__main__":
    main()