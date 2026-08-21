from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from snackstack.agents.prompts import MENU_AGENT_PROMPT
from snackstack.config import llm
from snackstack.logger import get_logger
from snackstack.state import SnackStackState
from snackstack.tools.menu_tools import search_menu_catalog

logger = get_logger("menu_agent")

menu_tools = [search_menu_catalog]
menu_tools_by_name = {t.name: t for t in menu_tools}
menu_llm = llm.bind_tools(menu_tools)


def menu_agent(state: SnackStackState) -> dict:
    """Call the menu LLM (with tools bound) and return a synthesizer payload."""
    user_query = state.get("user_query", "")
    task_desc = state.get("task_description", "Help with the menu")
    messages = [
        SystemMessage(content=MENU_AGENT_PROMPT),
        HumanMessage(content=f"Task: {task_desc}\nCustomer query: {user_query}"),
    ]
    response = menu_llm.invoke(messages)
    if response.tool_calls:
        messages.append(response)
        for call in response.tool_calls:
            tool = menu_tools_by_name[call["name"]]
            result = tool.invoke(call["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
        response = menu_llm.invoke(messages)

    logger.info("[menu:model] tool_calls=%s", bool(response.tool_calls))
    return {
        "messages": [response],
        "agent_results": [{"source": "menu_agent", "response": response.content}],
    }
