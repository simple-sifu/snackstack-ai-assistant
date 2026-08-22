from snackstack.agents.prompts import SYNTHESIZER_PROMPT
from snackstack.config import llm
from snackstack.logger import get_logger
from snackstack.state import SnackStackState

logger = get_logger("synthesizer")


def synthesizer_node(state: SnackStackState) -> dict:
    """Merge results from one or more agents into a single user-facing reply."""
    results = state.get("agent_results", [])
    user_query = state.get("user_query", "")

    if not results:
        logger.warning("Synthesizer received no agent results")
        return {"final_answer": "Sorry, I couldn't process that request. Please try again."}

    if len(results) == 1:
        logger.info("Synthesizer  single-agent pass-through")
        return {"final_answer": results[0]["response"]}

    logger.info("Synthesizer  merging %d agent responses", len(results))
    parts = "\n\n".join(
        f"[{r['source'].upper()}]:\n{r['response']}" for r in results
    )
    prompt = SYNTHESIZER_PROMPT.format(user_query=user_query, parts=parts)
    logger.info("Invoking llm synthesizer")
    
    merged = llm.invoke(prompt)
    return {"final_answer": merged.content}
