from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from snackstack.agents.prompts import ORDER_AGENT_PROMPT
from snackstack.config import llm
from snackstack.logger import get_logger
from snackstack.state import SnackStackState
from snackstack.tools.order_tools import get_order_status

logger = get_logger("order_agent")

order_tools = [get_order_status]
order_tools_by_name = {t.name: t for t in order_tools}
order_llm = llm.bind_tools(order_tools)


def order_agent(state: SnackStackState) -> dict:
    """Call the order LLM (with tools bound) and return a synthesizer payload."""
    user_query = state.get("user_query", "")
    task_desc = state.get("task_description", "Help with the order")
    messages = list(state.get("messages") or [])
    if not messages:
        messages = [
            SystemMessage(content=ORDER_AGENT_PROMPT),
            HumanMessage(content=f"Task: {task_desc}\nCustomer query: {user_query}"),
        ]
    response = order_llm.invoke(messages)
    if response.tool_calls:
        messages.append(response)
        for call in response.tool_calls:
            tool = order_tools_by_name[call["name"]]
            result = tool.invoke(call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
        response = order_llm.invoke(messages)

    logger.info("[order:model] tool_calls=%s", bool(response.tool_calls))
    return {
        "messages": [response],
        "agent_results": [{"source": "order_agent", "response": response.content}],
    }
