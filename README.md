# LLM & Agent Patterns

This repository contains implementations of common design patterns and workflows for Large Language Model (LLM) applications using LangGraph and an LLM model, following [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents). Each pattern demonstrates a specific way to structure LLM interactions for different use cases.

For the purpose for this example, I used Anthropic's Claude, but you are able to switch to other LLMs.

1. [Augmented LLM](#1-augmented-llm)
2. [Prompt Chaining](#2-prompt-chaining)
3. [Parallel Processing](#3-parallel-processing)
4. [Routing](#4-routing)
5. [Orchestrator-Worker](#5-orchestrator-worker)
6. [Evaluator-Optimizer](#6-evaluator-optimizer)

## 1. Augmented LLM

This pattern enhances LLM capabilities through structured outputs and tool integration.

### Features:

- Structured Output Generation
- Tool/Function Calling

### Use Cases:

1. **Search Query Optimization**

```python
# Using Pydantic model:
class SearchQuery(BaseModel):
    search_query: str  # Query optimized for web search
    justification: str # Why this query is important

output: SearchQuery = structured_llm.invoke("What is the capital of Israel?")
# Example output:
# SearchQuery(
#     search_query='capital of Israel',
#     justification='I need to find the capital of Israel for a project.'
# )
```

2. **Math Operations**

```python
message = llm_with_tools.invoke("What is 2 times 3 and 9 plus 8?")
# message.tool_calls has type List[Dict]:
# [
#  {'name': 'multiply',
#   'args': {'a': 2, 'b': 3},
#   'type': 'tool_call'},
#  {'name': 'add',
#   'args': {'a': 9, 'b': 8},
#   'type': 'tool_call'}
# ]
```

## 2. Prompt Chaining

Chains multiple LLM calls together in a sequential workflow with conditional branching.

### Features:

- Sequential Processing
- Conditional Branching
- State Management

### Use Cases:

1. **Joke Generation Pipeline**

```python
class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str

state: State = chain.invoke({"topic": "cats"})
# Example state:
# {
#     "topic": "cats",
#     "joke": "...",
#     "improved_joke": "...",
#     "final_joke": "..."
# }
```

## 3. Parallel Processing

Executes multiple LLM tasks concurrently and aggregates results.

### Features:

- Concurrent Task Execution
- Result Aggregation
- Independent Processing

### Use Cases:

1. **Creative Content Generation**

```python
class State(TypedDict):
    topic: str
    joke: str
    story: str
    poem: str
    aggregated_outputs: str

state: State = parallel_chain.invoke({"topic": "rugelach"})
# Example state:
# {
#     "topic": "rugelach",
#     "joke": "...",
#     "story": "...",
#     "poem": "...",
#     "aggregated_outputs": "Joke: ...\n\nStory: ...\n\nPoem: ..."
# }
```

## 4. Routing

Intelligently routes requests to appropriate handlers based on content analysis.

### Features:

- Content-based Routing
- Dynamic Handler Selection
- Structured Decision Making

### Use Cases:

1. **Creative Writing Assistant**

```python
class State(TypedDict):
    input: str
    route: Literal["joke", "story", "poem"]
    output: str

state: State = router_chain.invoke({"input": "I want to hear a joke"})
# Example state:
# {
#     "input": "I want to hear a joke.",
#     "route": "joke",
#     "output": "..."
# }
```

## 5. Orchestrator-Worker

Implements a distributed workflow where an orchestrator plans tasks and workers execute them.

### Features:

- Task Planning
- Parallel Execution
- Result Aggregation

### Use Cases:

1. **Report Generation**

```python
class Section(BaseModel):
    name: str    # Name of the section
    description: str  # Overview of topics covered

class State(TypedDict):
    topic: str
    sections: List[Section]
    completed_sections: List[str]
    final_report: str

state: State = orchestrator_worker.invoke({
    "topic": "Introduction to Model Context Providers"
})
# Example state:
# {
#     "topic": "Introduction to Model Context Providers",
#     "sections": [{"name": "Overview", "description": "..."}, ...],
#     "completed_sections": ["Section 1 content", "Section 2 content", ...],
#     "final_report": "Complete markdown report..."
# }
```

## 6. Evaluator-Optimizer

Implements a feedback loop to continuously improve outputs based on evaluation.

### Features:

- Output Generation
- Quality Evaluation
- Feedback-based Optimization

### Use Cases:

1. **Suggestion Optimization**

```python
class Feedback(BaseModel):
    status: Literal["useful", "not useful"]
    feedback: str

class State(TypedDict):
    topic: str
    suggestion: str | None
    feedback: str | None
    status: Literal["useful", "not useful"] | None

state: State = optimizer.invoke({
    "topic": "How can I stay hydrated all day long?"
})
# Example state:
# {
#     "topic": "How can I stay hydrated all day long?",
#     "suggestion": "# Staying Hydrated All Day\n- Start with a glass...",
#     "feedback": "This suggestion provides a comprehensive...",
#     "status": "useful"
# }
```

## 7. Agent

You can read more about it in this [dedicated README file](/workflows/7_agent/README.md).

## Setup

1. Install dependencies:

```bash
pip install langchain langchain-anthropic langgraph pydantic
```

2. Configure API keys in `config.py`:

```python
API_KEYS = {
    "ANTHROPIC": "your-api-key-here"
}
```

## Requirements

- Python 3.13
- Claude 3.5 + 3.7 Sonnet (via Anthropic API)
- LangChain
- LangGraph
- Pydantic

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
