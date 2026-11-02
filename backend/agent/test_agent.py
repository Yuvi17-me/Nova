import os
import sys
from pathlib import Path

# Add project root to sys.path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.agent.agent_core import AgentCore


agent = AgentCore()


tests = [
    "find my resume",
    "find resume",
    "search for my resume",
    "where is my resume",
    "open my downloads",
    "open my resume",
    "resume music",
    "resume video",
    "resume playback",
    "resume",
    "pause",
]


for message in tests:

    print()
    print("User:", message)

    result = agent.process(
        message
    )

    print("Agent:", result)