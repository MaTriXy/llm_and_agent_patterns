import json
import operator
import os
from typing import Annotated, List, TypedDict

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


# Report schema
class Section(BaseModel):
    name: str = Field(description="The name of this section of the report.")
    description: str = Field(
        description="The brief overview of the main topics and concepts covered in this section."
    )


class Sections(BaseModel):
    sections: List[Section] = Field(
        description="A list of sections that make up the full report."
    )


# LangGraph state
class State(TypedDict):
    topic: str
    sections: List[Section]
    completed_sections: Annotated[List[str], operator.add]
    final_report: str


class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[
        List[str], operator.add
    ]  # Each of the workers handle their own input, but all write out to the same completed sections list in parallel


def orchestrator(state: State):
    """Orchestrator function that plans the report."""

    planner = llm.with_structured_output(Sections)
    report_sections: Sections = planner.invoke(
        [
            SystemMessage(
                content="You are an expert journalistic writer. Generate a plan for a report."
            ),
            HumanMessage(content=f"Here is the topic of the report: {state["topic"]}"),
        ]
    )
    return {"sections": report_sections.sections}


def worker(state: WorkerState):
    """Worker function that writes one section of the report."""

    section = llm.invoke(
        [
            SystemMessage(
                content="You are an expert report writer. Write a section for a report."
            ),
            HumanMessage(
                content=f"Here is the name of the section: {state["section"].name}, and the description of the section: {state["section"].description}."
            ),
        ]
    )
    return {"completed_sections": [section.content]}


def aggregator(state: State):
    """Aggregator function that combines the completed sections into a final report."""

    return {"final_report": "\n\n".join(state["completed_sections"])}


def spawn_workers(state: State):
    """Spawn a worker for each section of the report."""

    return [Send("worker", {"section": section}) for section in state["sections"]]


orchestrator_worker_builder = StateGraph(State)

orchestrator_worker_builder.add_node("orchestrator", orchestrator)
orchestrator_worker_builder.add_node("worker", worker)
orchestrator_worker_builder.add_node("aggregator", aggregator)

orchestrator_worker_builder.add_edge(START, "orchestrator")
orchestrator_worker_builder.add_conditional_edges(
    "orchestrator", spawn_workers, ["worker"]
)
orchestrator_worker_builder.add_edge("worker", "aggregator")
orchestrator_worker_builder.add_edge("aggregator", END)

orchestrator_worker = orchestrator_worker_builder.compile()

state = orchestrator_worker.invoke(
    {
        "topic": "Introduction to the concept of Model Context Provider, and how it can be used for agentic AI workflows."
    }
)

with open(os.path.join(os.path.dirname(__file__), "final_report.md"), "w") as f:
    f.write(state["final_report"])
