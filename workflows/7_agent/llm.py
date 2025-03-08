from langchain_anthropic import ChatAnthropic

import config

from .tools import tools

llm = ChatAnthropic(
    model="claude-3-7-sonnet-20250219",
    api_key=config.API_KEYS["ANTHROPIC"],
)


llm_with_tools = llm.bind_tools(tools)
