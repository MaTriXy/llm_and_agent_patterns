from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel
from typing_extensions import TypedDict

import config

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", api_key=config.API_KEYS["ANTHROPIC"]
)


class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str


def generate_joke(state: State):
    message = llm.invoke(f"Write a joke about {state.get("topic")}")
    return {"joke": message.content}


def improve_joke(state: State):
    message = llm.invoke(
        f"Make this joke funnier by adding punchlines: {state.get("joke")}"
    )
    return {"improved_joke": message.content}


def polish_joke(state: State):
    message = llm.invoke(
        f"Add a surprising twist to this joke: {state.get("improved_joke")}"
    )
    return {"final_joke": message.content}


class FunnyCheck(BaseModel):
    funny_enough: bool


def funny_enough(state: State):
    structured_llm = llm.with_structured_output(FunnyCheck)
    message: FunnyCheck = structured_llm.invoke(
        f"Is this joke funny enough? {state.get("joke")}"
    )
    return message.funny_enough


workflow = StateGraph(State)

workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("polish_joke", polish_joke)

workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges(
    "generate_joke",
    funny_enough,
    {
        True: "improve_joke",
        False: END,
    },
)
workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)

chain = workflow.compile()

state = chain.invoke({"topic": "cats"})

state
# Example `state`:
# {
#     "topic": "cats",
#     "joke": "...",
#     "improved_joke": "...",
#     "final_joke": "...",
# }
