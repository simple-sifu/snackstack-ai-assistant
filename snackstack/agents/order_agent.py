from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.types import Command, Send, interrupt

from snackstack.agents.prompts import ORDER_AGENT_PROMPT
from snackstack.config import llm
from snackstack.logger import get_logger
from snackstack.state import SnackStackState
from snackstack.tools.order_tools import get_order_status

logger = get_logger("order_agent")

order_tools = [get_order_status]
order_tools_by_name = {t.name: t for t in order_tools}
order_llm = llm.bind_tools(order_tools)


def _ask_user(prompt: str) -> str:
    """Pause for HITL inside a graph; fall back to input() in a direct call."""
    try:
        return str(interrupt(prompt))
    except RuntimeError:
        return input(f"Agent asks: {prompt}\nYou: ").strip()


def order_agent(state: SnackStackState) -> dict:
    """Call the order LLM (with tools bound) and return a synthesizer payload."""
    user_query = state.get("user_query", "")
    task_desc = state.get("task_description", "Help with the order")
    messages = [
        SystemMessage(content=ORDER_AGENT_PROMPT),
        HumanMessage(content=f"Task: {task_desc}\nCustomer query: {user_query}"),
    ]
    response = order_llm.invoke(messages)

    if not response.tool_calls:
        logger.info("[order:model] HITL: interrupting to collect user info")
        user_reply = _ask_user(str(response.content))
        logger.info("[order:model] HITL: user replied %r", user_reply)
        messages.append(response)
        messages.append(HumanMessage(content=str(user_reply)))
        response = order_llm.invoke(messages)
        logger.info("[order:model] HITL: response=%r", response)

    max_tool_calls = 5
    if response.tool_calls:
        messages.append(response)
        for call in response.tool_calls[:max_tool_calls]:
            tool = order_tools_by_name[call["name"]]
            result = tool.invoke(call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
        response = order_llm.invoke(messages)

    logger.info("[order:model] tool_calls=%s", bool(response.tool_calls))
    logger.info("[order:model] final response=%r", response.content)
    return {
        "agent_results": [{"source": "order_agent", "response": response.content}]
    }

