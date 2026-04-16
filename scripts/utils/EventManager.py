import asyncio
import threading
from ..core.Enums import Events


class EventManager:
    def __init__(self):
        self._listeners = { event:[] for event in Events}
        self._last_event_data = {}
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
            self._last_event_data[event_type] = data
            print(f"Notifying {len(self._listeners[event_type])} listeners of event '{event_type.name}' with data: {data}")
            for listener in list(self._listeners[event_type]):
                result = listener(data)
                if asyncio.iscoroutine(result):
                    asyncio.run_coroutine_threadsafe(result, self._loop)

    async def wait_for(self, event_type):
        if event_type in self._last_event_data:
            return self._last_event_data[event_type]

        loop = asyncio.get_running_loop()
        future = loop.create_future()

        def listener(data):
            if not future.done():
                loop.call_soon_threadsafe(future.set_result, data)
            self.unsubscribe(event_type, listener)

        self.subscribe(event_type, listener)
        return await future

event_manager = EventManager()