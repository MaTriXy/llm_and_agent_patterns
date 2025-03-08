from langgraph.graph import END, START, MessagesState, StateGraph

from .workflow import llm_call, should_continue, tool_node

agent_builder = StateGraph(MessagesState)

agent_builder.add_node("llm", llm_call)
agent_builder.add_node("tools", tool_node)

agent_builder.add_edge(START, "llm")
agent_builder.add_conditional_edges(
    "llm", should_continue, {"USE_TOOLS": "tools", END: END}
)
agent_builder.add_edge("tools", "llm")

agent = agent_builder.compile()
