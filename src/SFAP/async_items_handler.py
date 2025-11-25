import asyncio
import traceback
from typing import Optional, Any

class AsyncItemsHandler:
    input_queue: asyncio.Queue[Any]
    stop_signal: asyncio.Event
    output_queue: Optional[asyncio.Queue[Any]]
    next_stage_signal: Optional[asyncio.Event]

    def __init__(self) -> None:
        self.input_queue = asyncio.Queue()
        self.stop_signal = asyncio.Event()
        self.output_queue = None
        self.next_stage_signal = None

    def link(self, next_stage: 'AsyncItemsHandler') -> 'AsyncItemsHandler':
        self.output_queue = next_stage.input_queue
        self.next_stage_signal = next_stage.stop_signal
        return next_stage

    async def process(self, item: Any) -> Any:
        print(f"self: {self} -> unimplemented: item process method: {item}")
        raise NotImplementedError

    async def run(self) -> None:
        while True:
            if self.stop_signal.is_set() and self.input_queue.empty():
                if self.next_stage_signal:
                    self.next_stage_signal.set()
                break
            try:
                item: Any = await asyncio.wait_for(self.input_queue.get(), timeout=0.1)
                result = await self.process(item)
                if result is not None and self.output_queue is not None:
                    await self.output_queue.put(result)
                self.input_queue.task_done()

            except asyncio.TimeoutError:
                continue

            except Exception:
                traceback.print_exc()
                continue
