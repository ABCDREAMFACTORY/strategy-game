import asyncio
import threading
from collections.abc import Callable
from typing import Any

from ..core.Enums import Events


class EventManager:
    def __init__(self):
        self._listeners: dict[Events, list[Callable[[Any], Any]]] = {event: [] for event in Events}
        self._event_store: dict[Events, dict[str, Any]] = {event: {"data": None, "event": asyncio.Event()} for event in Events}
        self._loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._loop_thread: threading.Thread = threading.Thread(target=self._run_loop, daemon=True)
        self._loop_thread.start()

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def subscribe(self, event_type: Events, listener: Callable[[Any], Any]) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type: Events, listener: Callable[[Any], Any]) -> None:
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def notify(self, event_type: Events, data: Any = None) -> None:
        if event_type in self._listeners:
            store = self._event_store[event_type]
            store["data"] = data
            self._loop.call_soon_threadsafe(store["event"].set)
            for listener in list(self._listeners[event_type]):
                result = listener(data)
                if asyncio.iscoroutine(result):
                    asyncio.run_coroutine_threadsafe(result, self._loop)

    async def wait_for(self, event_type: Events) -> Any:
        store = self._event_store[event_type]
        await store["event"].wait()
        return store["data"]

event_manager = EventManager()