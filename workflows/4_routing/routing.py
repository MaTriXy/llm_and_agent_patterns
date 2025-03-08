from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import Literal, TypedDict

import config

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", api_key=config.API_KEYS["ANTHROPIC"]
)

RouteType = Literal["joke", "story", "poem"]


class Route(BaseModel):
    route: RouteType = Field(None, description="The next step in the routing workflow.")


router = llm.with_structured_output(Route)


class State(TypedDict):
    input: str
    route: RouteType
    output: str


def write_story(state: State):
    story = llm.invoke(state.get("input"))
    return {"output": story.content}


def write_joke(state: State):
    joke = llm.invoke(state.get("input"))
    return {"output": joke.content}


def write_poem(state: State):
    poem = llm.invoke(state.get("input"))
    return {"output": poem.content}


def call_router(state: State):
    output: Route = router.invoke(
        [
            SystemMessage(
                content="Route the user's input to story, joke, or poem, based on the user's request."
            ),
            HumanMessage(content=state.get("input")),
        ]
    )
    return {"route": output.route}


def route(state: State):
    if state.get("route") == "story":
        return "write_story"
    elif state.get("route") == "joke":
        return "write_joke"
    elif state.get("route") == "poem":
        return "write_poem"


router_workflow = StateGraph(State)

router_workflow.add_node("write_story", write_story)
router_workflow.add_node("write_joke", write_joke)
router_workflow.add_node("write_poem", write_poem)
router_workflow.add_node("call_router", call_router)

router_workflow.add_edge(START, "call_router")
router_workflow.add_conditional_edges(
    "call_router",
    route,
    {
        "write_story": "write_story",
        "write_joke": "write_joke",
        "write_poem": "write_poem",
    },
)

router_workflow.add_edge("write_story", END)
router_workflow.add_edge("write_joke", END)
router_workflow.add_edge("write_poem", END)

router_chain = router_workflow.compile()

state = router_chain.invoke({"input": "I want to hear a joke."})

state
# Example `state`:
# {
#     "input": "I want to hear a joke.",
#     "route": "joke",
#     "output": "..."
# }
