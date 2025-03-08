from langchain_core.messages import HumanMessage

from .agent import agent

messages = [
    HumanMessage(
        content="""
        Can you please:

        1. List all of my invoices this month.
        2. Tell me which outgoing invoice has the highest amount.
        3. Also, show me which incoming invoice has the highest amount.
        4. Calculate the total amount of all invoices.
        5. Oh, almost forgot. I bought a new MacBook Pro for the office today and it cost 2,500$. Create me an invoice for that!

        Thanks!
        """
    )
]

state = {"messages": messages}

response = agent.invoke(state)

for message in response["messages"]:
    message.pretty_print()
