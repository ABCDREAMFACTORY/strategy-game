import asyncio
import threading
from ..core.Enums import Events


class EventManager:
    def __init__(self):
        self._listeners = { event:[] for event in Events}
        self._event_store = { event: {"data": None, "event": asyncio.Event()} for event in Events}
        self._loop = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(target=self._run_loop, daemon=True)
        self._loop_thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def subscribe(self, event_type, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def notify(self, event_type, data=None):
        if event_type in self._listeners:
            store = self._event_store[event_type]
            store["data"] = data
            self._loop.call_soon_threadsafe(store["event"].set)
            print(f"Notifying {len(self._listeners[event_type])} listeners of event '{event_type.name}' with data: {data}")
            for listener in list(self._listeners[event_type]):
                result = listener(data)
                if asyncio.iscoroutine(result):
                    asyncio.run_coroutine_threadsafe(result, self._loop)

    async def wait_for(self, event_type):
        store = self._event_store[event_type]
        await store["event"].wait()
        return store["data"]

event_manager = EventManager()