"""
LangGraph state definitions.

AxiomCartState       – the main graph state shared by all nodes.
WorkerInput          – the payload sent to agent workers via Send().
AgentTask            – structured routing output from the orchestrator.
ClassificationResult – orchestrator's full decision.
"""

from __future__ import annotations

import operator
from typing import Annotated, List, Literal, TypedDict

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field


def agent_results_reducer(current: list[dict], update: list[dict]) -> list[dict]:
    """Like operator.add, but an empty list signals a reset."""
    if not update:
        return []
    return current + update


class AgentTask(BaseModel):
    """A single task assigned to a specialist agent."""

    agent: Literal["menu_agent", "order_agent"] = Field(
        description="Which specialist should run this task. Use each agent at most once."
    )
    task_description: str = Field(
        description="What that agent should do for this query"
    )


class ClassificationResult(BaseModel):
    """Orchestrator's routing decision."""

    tasks: List[AgentTask] = Field(
        description=(
            "One task per agent that should run. "
            "Menu-only → [{menu_agent}]. Order-only → [{order_agent}]. "
            "Mixed pizza+order queries → exactly "
            "[{menu_agent}, {order_agent}]. Never repeat an agent."
        ),
        min_length=1,
        max_length=2,
    )
    requires_synthesis: bool = Field(
        description="True only when both menu_agent and order_agent have a task"
    )
    reasoning: str = Field(description="Brief explanation of routing decision")


class SnackStackState(TypedDict, total=False):
    """Top-level state that flows through the entire graph."""

    # Conversation
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    task_description: str

    # Routing
    route: Literal["menu_agent", "order_agent"]
    tasks: list[AgentTask]
    requires_synthesis: bool

    # Collected results from agents (operator.add merges parallel results)
    agent_results: Annotated[list[dict], agent_results_reducer]

    # Final response returned to the user
    final_answer: str
