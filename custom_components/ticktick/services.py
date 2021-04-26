from homeassistant.core import HomeAssistant, ServiceCall
from ticktick import api
from typing import Callable
from datetime import datetime
import logging


def handle_create_task(client: api.TickTickClient) -> Callable:
    def handler(call: ServiceCall):
        # Resolve dates
        due = call.data.get("due", None)
        start = call.data.get("start", None)
        end = call.data.get("end", None)
        if start:
            start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z") if end else None
        else:
            start = datetime.strptime(due, "%Y-%m-%d") if due else None
            end = None

        # Create task
        print(call.data.get("tags"))
        task = task = client.task.builder(
            call.data.get("name"),
            start=start,
            end=end,
            priority=call.data.get("priority", "none"),
            project=call.data.get("project", None),
            tags=call.data.get("tags", None),
            content=call.data.get("content", ""),
        )
        client.task.create([task])

    return handler


def register_services(
    DOMAIN: str, hass: HomeAssistant, client: api.TickTickClient
) -> None:
    hass.services.async_register(DOMAIN, "create_task", handle_create_task(client))
