from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field

import config

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", api_key=config.API_KEYS["ANTHROPIC"]
)


class SearchQuery(BaseModel):
    search_query: str = Field(
        None, description="Query that is optimized for web search."
    )
    justification: str = Field(
        None, description="Why this query is important to answer the user's question."
    )


structured_llm = llm.with_structured_output(SearchQuery)

output: SearchQuery = structured_llm.invoke("What is the capital of Israel?")

output
# Example `output`:
# SearchQuery(
#     search_query='capital of Israel',
#     justification='I need to find the capital of Israel for a project.'
# )
