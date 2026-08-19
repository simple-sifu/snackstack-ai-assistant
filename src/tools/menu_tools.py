"""
Agent Tools — the concrete actions agents can take.

Product Discovery (1 tool):
  • search_product_catalog  – RAG semantic search

"""

from __future__ import annotations

from langchain_core.tools import tool

from src.config import get_logger
from src.tools.rag import menu_search_vectorstore as menu_vectorstore

logger = get_logger("menu_tools")


# ═══════════════════════════════════════════════════════════
#  Menu DISCOVERY TOOL
# ═══════════════════════════════════════════════════════════

@tool
def search_menu_catalog(query: str) -> str:
    """Search the snackshack menu catalog using semantic search (RAG).

    Args:
        query: natural-language search, e.g. menu items under 300"
    """
    logger.info("search_menu_catalog  query=%r", query)
    try:
        docs = menu_vectorstore.similarity_search(query, k=3)
        if not docs:
            return "No menu items found matching your query."
        results = "Found the following products:\n\n"
        for i, doc in enumerate(docs, 1):
            results += f"Menu item {i}:\n{doc.page_content}\n\n"
        return results
    except Exception as exc:
        logger.exception("Catalog search failed")
        return f"Error searching catalog: {exc}"
