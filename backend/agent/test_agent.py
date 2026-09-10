from backend.agent.agent_core import AgentCore


agent = AgentCore()


tests = [
    # "find and open resume",
"open my downloads",
"open my My resume",
]


for message in tests:

    print()
    print("User:", message)

    result = agent.process(
        message
    )

    print("Agent:", result)