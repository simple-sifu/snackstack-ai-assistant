"""
RAG: Build a ChromaDB vector store from the menu catalog.

The vector store is created once at import time and re-used by the
search_menu_catalog tool.
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document

from snackstack.config import embeddings
from snackstack.logger import get_logger
from snackstack.data.menu import MENU_CATALOG

logger = get_logger("rag")


def _build_documents() -> list[Document]:
    """Convert every catalog entry into a LangChain Document."""
    docs: list[Document] = []
    for item in MENU_CATALOG:
        dietary = ", ".join(item["dietary_tags"]) or "None"
        content = (
            f"Dish: {item['name']}\n"
            f"Cuisine: {item['cuisine']}\n"
            f"Category: {item['category']}\n"
            f"Price: ₹{item['price']}\n"
            f"Rating: {item['rating']}/5\n"
            f"Dietary: {dietary}\n"
            f"Description: {item['description']}\n"
            f"Available: {'Yes' if item['availability'] else 'No'}"
        )
        docs.append(
            Document(
                page_content=content,
                metadata={
                    "id": item["id"],
                    "name": item["name"],
                    "cuisine": item["cuisine"],
                    "category": item["category"],
                    "price": item["price"],
                    "rating": item["rating"],
                },
            )
        )
    return docs


def build_vectorstore() -> Chroma:
    """Create an in-memory ChromaDB collection from the menu catalog."""
    docs = _build_documents()
    store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="snackshack_menu",
    )
    logger.info("Vector store ready  (%d menu indexed)", len(docs))
    return store


# Module-level singleton so every importer shares the same store
menu_search_vectorstore = build_vectorstore()
