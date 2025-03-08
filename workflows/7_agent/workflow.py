from typing import Literal

from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import END, MessagesState

from .llm import llm_with_tools
from .tools import tools_by_name


def llm_call(state: MessagesState) -> MessagesState:
    """Call the LLM with the tools. The response contains a decision whether to call a tool or not."""

    response = llm_with_tools.invoke(
        [
            SystemMessage(
                content="You are a helpful financial business assistant that can answer questions and perform actions with the following tools: "
                + ", ".join(tools_by_name.keys())
                + "."
            ),
        ]
        + state["messages"]
    )

    return {"messages": [response]}


def tool_node(state: MessagesState) -> MessagesState:
    """Execute the tool calls from the last message, and append the results."""

    tool_results = []
    last_tool_calls = state["messages"][-1].tool_calls or []

    for tool_call in last_tool_calls:
        id = tool_call["id"]
        name = tool_call["name"]
        args = tool_call["args"]

        tool = tools_by_name[name]
        tool_result: str = tool.invoke(args)

        tool_results.append(
            ToolMessage(
                content=tool_result,
                tool_call_id=id,
                name=name,
            )
        )

    return {"messages": tool_results}


def should_continue(state: MessagesState):
    """Decide if the agent should continue the workflow or stop, based on whether the LLM has decided to stop calling tools."""

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "USE_TOOLS"
    else:
        return END
