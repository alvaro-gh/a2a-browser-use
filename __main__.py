"""Main A2A Server."""

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from login_executor import LoginAgentExecutor

if __name__ == "__main__":
    skill = AgentSkill(
        id="login",
        name="Logs in to Site",
        description="Checks if cookie is present and logs in if necessary",
        tags=["login"],
        examples=["Login to linkedin", "login"],
    )

    public_agent_card = AgentCard(
        name="Login Agent",
        description="Agent to log in to site using user and password",
        url="http://127.0.0.1:9999/",
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
        supportsAuthenticatedExtendedCard=False,
    )

    request_handler = DefaultRequestHandler(
        agent_executor=LoginAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host="127.0.0.1", port=9999)
