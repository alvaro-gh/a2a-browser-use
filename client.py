"""Main A2A Client."""

import logging
from typing import Any
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
)


async def main() -> None:
    """Run the main loop."""
    public_agent_card_path = "/.well-known/agent.json"

    # Configure logging to show INFO level messages
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)  # Get a logger instance

    base_url = "http://127.0.0.1:9999"

    async with httpx.AsyncClient(timeout=60) as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
        )

        final_agent_card_to_use: AgentCard | None = None

        logger.info(
            "Attempting to fetch public agent card from: %s%s",
            base_url,
            public_agent_card_path,
        )
        _public_card = await resolver.get_agent_card()
        logger.info("Successfully fetched public agent card:")
        logger.info(_public_card.model_dump_json(indent=2, exclude_none=True))
        final_agent_card_to_use = _public_card
        logger.info(
            "\nUsing PUBLIC agent card for client initialization (default).",
        )

        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=final_agent_card_to_use,
        )
        logger.info("A2AClient initialized.")

        send_message_payload: dict[str, Any] = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": ""}],
                "messageId": uuid4().hex,
            },
        }
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**send_message_payload),
        )

        response = await client.send_message(request)
        print(response.model_dump(mode="json", exclude_none=True))  # noqa: T201

        streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**send_message_payload),
        )

        stream_response = client.send_message_streaming(streaming_request)

        async for chunk in stream_response:
            print(chunk.model_dump(mode="json", exclude_none=True))  # noqa: T201


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
