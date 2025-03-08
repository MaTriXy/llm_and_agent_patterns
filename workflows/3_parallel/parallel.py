from typing import TypedDict

from langchain_anthropic import ChatAnthropic
from langgraph.graph import END, START, StateGraph

import config

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", api_key=config.API_KEYS["ANTHROPIC"]
)


class State(TypedDict):
    topic: str
    joke: str
    story: str
    poem: str
    aggregated_outputs: str


def write_joke(state: State):
    message = llm.invoke(f"Write a joke about {state.get("topic")}")
    return {"joke": message.content}


def write_story(state: State):
    message = llm.invoke(f"Write a story about {state.get("topic")}")
    return {"story": message.content}


def write_poem(state: State):
    message = llm.invoke(f"Write a poem about {state.get("topic")}")
    return {"poem": message.content}


def aggregator(state: State):
    aggregated_outputs = f"Joke: {state.get("joke")}\n\nStory: {state.get("story")}\n\nPoem: {state.get("poem")}"
    return {"aggregated_outputs": aggregated_outputs}


parallel_workflow = StateGraph(State)

parallel_workflow.add_node("write_joke", write_joke)
parallel_workflow.add_node("write_story", write_story)
parallel_workflow.add_node("write_poem", write_poem)
parallel_workflow.add_node("aggregator", aggregator)

parallel_workflow.add_edge(START, "write_joke")
parallel_workflow.add_edge(START, "write_story")
parallel_workflow.add_edge(START, "write_poem")
parallel_workflow.add_edge("write_joke", "aggregator")
parallel_workflow.add_edge("write_story", "aggregator")
parallel_workflow.add_edge("write_poem", "aggregator")
parallel_workflow.add_edge("aggregator", END)

parallel_chain = parallel_workflow.compile()

state = parallel_chain.invoke({"topic": "rugelach"})

state
# Example `state`:
# {
#     "topic": "cats",
#     "joke": "...",
#     "story": "...",
#     "poem": "...",
#     "aggregated_outputs": "..."
# }
