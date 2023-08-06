from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any, Protocol

from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)


class EventHandler(Protocol):
    async def __call__(self, data: bytes) -> None:  # noqa: U100  # false alarm
        pass


class RabbitConsumer:
    def __init__(self, queue: str) -> None:
        self.queue_name: str = queue
        self.handlers: dict[str | None, EventHandler] = {}

    def on_event(
        self, event_name: str | None = None
    ) -> Callable[[EventHandler], EventHandler]:
        def on_event_wrapper(function: EventHandler) -> EventHandler:
            self.handlers[event_name] = function
            return function

        return on_event_wrapper

    async def handle_event(self, message: AbstractIncomingMessage) -> None:
        logging.debug(f"New message", extra={"original_message": message})

        event_header: Any | None = message.headers.get("event_name")
        if event_header is not None and not isinstance(event_header, str):
            await message.reject()
            logging.warning(f"Wrong header type '{type(event_header)}'")
            return

        event_name: str = event_header
        handler: EventHandler | None = self.handlers.get(event_name)
        if handler is None:
            await message.reject()
            logging.warning(f"Wrong name '{event_name}'")
            return

        try:
            logging.info(f"Start processing event '{event_name}'")
            await handler(message.body)
        except Exception as exc:
            await message.reject()
            logging.error(
                "Error while handling event",
                exc_info=exc,
                extra={"event_name": event_name, "original_message": message},
            )
            return
        await message.ack()

    async def run(self, connection: AbstractConnection) -> None:
        channel: AbstractChannel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue: AbstractQueue
        queue = await channel.declare_queue(self.queue_name)
        await queue.consume(self.handle_event)
