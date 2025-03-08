import json
import operator
import os
from typing import Annotated, List, Literal, TypedDict

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

import config

llm = ChatAnthropic(
    model="claude-3-7-sonnet-20250219",
    api_key=config.API_KEYS["ANTHROPIC"],
)


class Feedback(BaseModel):
    status: Literal["useful", "not useful"] = Field(
        description="The grade of the suggestion, either useful or not useful."
    )
    feedback: str = Field(
        description="The feedback on the suggestion, either positive or negative."
    )


class State(TypedDict):
    topic: str
    suggestion: str | None = None
    feedback: str | None = None
    status: Literal["useful", "not useful"] | None = None


def suggestion_generator_llm(state: State):
    """Generate a suggestion for a given topic."""

    if state.get("feedback"):
        response = llm.invoke(
            f"Write a quick and short suggestion for the given topic: {state['topic']}. Take into account the feedback: {state['feedback']}"
        )
    else:
        response = llm.invoke(
            f"Write a quick and short suggestion for the given topic: {state['topic']}"
        )

    return {"suggestion": response.content}


def suggestion_evaluator_llm(state: State):
    """Evaluate the suggestion for the given topic."""

    evaluator = llm.with_structured_output(Feedback)
    response = evaluator.invoke(
        f'Evaluate the suggestion: "{state["suggestion"]}" for the given topic: "{state["topic"]}"'
    )

    return {"feedback": response.feedback, "status": response.status}


def route_suggestion(state: State):
    """Route the tip to the appropriate worker."""

    if state.get("status") == "not useful":
        return "FEEDBACK"
    elif state.get("status") == "useful":
        return "OK"


optimizer_builder = StateGraph(State)

optimizer_builder.add_node("suggestion_generator", suggestion_generator_llm)
optimizer_builder.add_node("suggestion_evaluator", suggestion_evaluator_llm)

optimizer_builder.add_edge(START, "suggestion_generator")
optimizer_builder.add_edge("suggestion_generator", "suggestion_evaluator")
optimizer_builder.add_conditional_edges(
    "suggestion_evaluator",
    route_suggestion,
    {"OK": END, "FEEDBACK": "suggestion_generator"},
)

optimizer = optimizer_builder.compile()

state = optimizer.invoke(
    {
        "topic": "How can I stay hydrated all day long?",
    }
)


with open(os.path.join(os.path.dirname(__file__), "suggestion.md"), "w") as f:
    f.write(state["suggestion"])

with open(os.path.join(os.path.dirname(__file__), "state.json"), "w") as f:
    json.dump(state, f)
