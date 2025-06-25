"""Login to Linkedin Agent."""

import os

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from browser_use import Agent, BrowserSession
from langchain_openai import ChatOpenAI


class LoginAgent:
    """Login to Site."""

    async def invoke(self) -> None | str:
        """Invoke Login Agent."""
        user = os.getenv("LINKEDIN_USER")
        pswd = os.getenv("LINKEDIN_PASSWORD")
        session = BrowserSession(
            storage_state="./data/state.json",
            user_data_dir=None,
            headless=True,
        )
        agent = Agent(
            task=f"""
              Go to linkedin.com and check if the user is logged in.
              If the user is not logged then log in using the following credentials:
              - Email: {user}
              - Password (inside the quotes): '{pswd}'
              If the user is already logged in do nothing.
              """,
            llm=ChatOpenAI(model="gpt-4o"),
            browser_session=session,
        )
        history = await agent.run()
        return history.final_result()


class LoginAgentExecutor(AgentExecutor):
    """Login to Site Executor."""

    def __init__(self) -> None:
        """Init this Executor."""
        self.agent = LoginAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute this Agent."""
        result: str | None = await self.agent.invoke()
        if result is None:
            result = "We seem to be unable to provide an answer right now"
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self) -> None:
        """Cancel the execution."""
        raise Exception("cancel not supported")
