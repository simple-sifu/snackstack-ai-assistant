import sys

# Stage 1: Foundation
# from snackstack.config import llm
# print(llm.invoke("Hello, how are you?").content)
# sys.exit()


# Stage 2 - RAG - Menu Search Tool
# from snackstack.tools import search_menu_catalog
# print(search_menu_catalog.invoke({"query": "pizza"}))
# sys.exit()

# Stage 3 - RAG - Order Search Tool
# from snackstack.tools import get_order_status
# print(get_order_status.invoke({"identifier": "sneha@example.com"}))
# sys.exit()

# Stage 4 - Orchestrator Agent
# from snackstack.agents.orchestrator import orchestrator_node
# print(orchestrator_node(
#     {"user_query": "what kind of pizza do you have and where is my order?"}
# ))
# sys.exit()

# Stage 5 - Menu Agent
# from snackstack.agents.menu_agent import menu_agent
# print(menu_agent({"user_query": "what kind of pizza do you have?"}))
# sys.exit()

# Stage 6 - Order Agent
# from snackstack.agents.order_agent import order_agent
# print(order_agent({"user_query": "What is the status of order ORD-203?"}))
# sys.exit()

# Stage 7 - Order Agent HITL
# from langchain_core.runnables import RunnableConfig
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import END, START, StateGraph
# from langgraph.types import Command

# from snackstack.agents.order_agent import order_agent
# from snackstack.agents.synthesizer import synthesizer_node
# from snackstack.state import SnackStackState

# builder = StateGraph(SnackStackState)
# builder.add_node("order_agent", order_agent)
# builder.add_node("synthesizer", synthesizer_node)
# builder.add_edge(START, "order_agent")
# builder.add_edge("synthesizer", END)
# hitl_graph = builder.compile(checkpointer=MemorySaver())

# cfg: RunnableConfig = {"configurable": {"thread_id": "test-hitl"}}
# result = hitl_graph.invoke(
#     {"user_query": "What is the status of my order?"},
#     cfg,
# )
# while result.get("__interrupt__"):
#     question = result["__interrupt__"][0].value
#     answer = input(f"Agent asks: {question}\nYou: ").strip()
#     result = hitl_graph.invoke(Command(resume=answer), cfg)
# print(result.get("final_answer", result))
# sys.exit()


# Stage 8 - Synthesizer + full Graph
# from langchain_core.messages import HumanMessage
# from langchain_core.runnables import RunnableConfig
# from langgraph.types import Command
# from snackstack.graph import snackstack_graph
# cfg: RunnableConfig = {"configurable": {"thread_id": "test-006"}}
# result = snackstack_graph.invoke(
#     {
#         "messages": [HumanMessage(content="show me status of my order. Also do you have any indian snacks?")],
#         "user_query": "show me status of my order. Also do you have any indian food?",
#     },
#     cfg,
# )
# while result.get("__interrupt__"):
#     question = result["__interrupt__"][0].value
#     answer = input(f"Agent asks: {question}\nYou: ").strip()
#     result = snackstack_graph.invoke(Command(resume=answer), cfg)
# print(result.get("final_answer") or result.get("agent_results"))

# Stage 8
# from snackstack.main import main
# main()  # text REPL
# sys.exit()


# Stage 9
from snackstack.main import main
sys.argv[1:] = ["--voice"]
main()  # voice mode
sys.exit()

