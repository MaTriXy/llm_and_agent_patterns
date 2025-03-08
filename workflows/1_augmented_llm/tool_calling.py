from langchain_anthropic import ChatAnthropic

import config

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", api_key=config.API_KEYS["ANTHROPIC"]
)


def multiply(a: int, b: int) -> int:
    return a * b


def add(a: int, b: int) -> int:
    return a + b


llm_with_tools = llm.bind_tools([multiply, add])

message = llm_with_tools.invoke("What is 2 times 3 and 9 plus 8?")

message.tool_calls
# Example `message.tool_calls`:
# [
#  {'name': 'multiply',
#   'args': {'a': 2, 'b': 3},
#   'type': 'tool_call'},
#  {'name': 'add',
#   'args': {'a': 9, 'b': 8},
#   'type': 'tool_call'}
#  ]
