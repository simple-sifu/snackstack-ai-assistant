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
# print(get_order_status.invoke({"identifier": "ORD-202"}))
# sys.exit()

# Stage 3 - Product Agent Subgraph
# from langchain_core.messages import HumanMessage, SystemMessage
# from src.nodes import product_subgraph, PRODUCT_PROMPT
# result = product_subgraph.invoke({'messages': [
#     SystemMessage(content=PRODUCT_PROMPT),
#     HumanMessage(content='Show me headphones under 15000')]})
# print(result['messages'][-1].content)
# sys.exit()


# Stage 4 - Support Agent + Tools
# from langchain_core.messages import HumanMessage, SystemMessage
# from src.nodes import support_subgraph, SUPPORT_PROMPT
# result = support_subgraph.invoke({'messages': [
#     SystemMessage(content=SUPPORT_PROMPT),
#     HumanMessage(content='Status of order ORD102?')]})
# print(result['messages'][-1].content)
# sys.exit()


# Stage 5 - Orchestrator + Multi-Agent Routing
# from src.config import llm
# from src.state import ClassificationResult
# c = llm.with_structured_output(ClassificationResult)
# r = c.invoke('Classify: My order ORD102 is late show me alternatives')
# print(r)
# print('Mixed:', [t.agent for t in r.tasks], 'synthesis:', r.requires_synthesis)
# sys.exit()


# Stage 6 - Synthesizer + full Graph
# from langchain_core.messages import HumanMessage
# from src.graph import axiomcart_graph
# result = axiomcart_graph.invoke(
#     {'messages': [HumanMessage(content='ORD102 is late, show me headphones')],
#     'user_query': 'ORD102 is late, show me headphones'},
#     {'configurable': {'thread_id': 'test-006'}})
# print(result['final_answer'])
# sys.exit()

# Stage 7 - Human in the Loop (HITL) 
# from langchain_core.messages import HumanMessage
# from langchain_core.runnables import RunnableConfig
# from langgraph.types import Command
# from src.graph import axiomcart_graph
# cfg: RunnableConfig = {'configurable': {'thread_id': 'test-hitl'}}
# r = axiomcart_graph.invoke(
#     {'messages': [HumanMessage(content='where is my order?')],
#      'user_query': 'Where is my order'}, cfg)
# while '__interrupt__' in r and r['__interrupt__']:
#     answer = input(f"Agent asks: {r['__interrupt__'][0].value}\nYou: ").strip()
#     r = axiomcart_graph.invoke(Command(resume=answer), cfg)
# print(r['final_answer'])
# sys.exit()



# Stage 8
# python -m src.main # text REPL
# python -m src.main --voice # voice mode
