from typing import Literal

from langgraph.types import Command, Send
from snackstack.config import llm
from snackstack.logger import get_logger
from snackstack.state import AgentTask, ClassificationResult, SnackStackState
from snackstack.agents.prompts import ORCHESTRATOR_PROMPT   

logger = get_logger("orchestrator")


def orchestrator_node(state: SnackStackState) -> Command[Literal["menu_agent", "order_agent", "synthesizer"]]:
    """Classify the user query and dispatch to the right agent(s).

    Args:
        state: The current state of the snackstack.

    Returns:
        A command to dispatch to the right agent(s).
    """
    user_query = state.get("user_query", "")
    if not user_query and state.get("messages"):
        user_query = state["messages"][-1].content

    logger.info("Orchestrator  query=%r", user_query)

    classifier = llm.with_structured_output(ClassificationResult)
    try:
        logger.info("Invoking llm classifier")
        classification = classifier.invoke(
            ORCHESTRATOR_PROMPT.format(user_query=user_query)
        )
    except Exception:
        logger.exception("Classification failed — defaulting to support_agent")
        classification = ClassificationResult(
            tasks=[], requires_synthesis=False,
            reasoning="Fallback: classification error",
        )

    logger.info("\n  routing=%s\n  reasoning=%s\n synthesis=%s\n",
                [t.agent for t in classification.tasks],
                classification.reasoning,
                classification.requires_synthesis)

    targets: list[Send] = []
    for task in classification.tasks:
        targets.append(Send(task.agent, {
            "messages": state.get("messages", []),
            "user_query": user_query,
            "task_description": task.task_description,
        }))

    if not targets:
        targets = [Send("synthesizer", {})]

    return Command(
        update={
            "tasks": classification.tasks,
            "requires_synthesis": classification.requires_synthesis,
            "user_query": user_query,
            "agent_results": [],  # reset stale results from prior turns
        },
        goto=targets,
    )