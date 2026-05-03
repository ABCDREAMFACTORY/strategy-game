import asyncio
import threading
from collections.abc import Callable
from typing import Any

from ..core.Enums import Events


class EventManager:
    def __init__(self):
        self._listeners: dict[Events, list[Callable[[Any], Any]]] = {event: [] for event in Events}

    def subscribe(self, event_type: Events, listener) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type: Events, listener: Callable[[Any], Any]) -> None:
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def notify(self, event_type: Events, data: Any = None) -> None:
        print(f"Event triggered: {event_type}, data: {data}")
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(data)
                
event_manager = EventManager()