import asyncio
import traceback
from typing import Optional, Any, Set

class AsyncItemsHandler:
    input_queue: asyncio.Queue[Any]
    stop_signal: asyncio.Event
    output_queue: Optional[asyncio.Queue[Any]]
    next_stage_signal: Optional[asyncio.Event]

    def __init__(self, concurrency: int = 1) -> None:
        self.input_queue = asyncio.Queue()
        self.stop_signal = asyncio.Event()
        self.output_queue = None
        self.next_stage_signal = None
        self.semaphore = asyncio.Semaphore(concurrency)
        self.active_tasks: Set[asyncio.Task[Any]] = set()

    def link(self, next_stage: 'AsyncItemsHandler') -> 'AsyncItemsHandler':
        self.output_queue = next_stage.input_queue
        self.next_stage_signal = next_stage.stop_signal
        return next_stage

    async def process(self, item: Any) -> Any:
        print(f"self: {self} -> unimplemented: item process method: {item}")
        raise NotImplementedError

    async def _process_wrapper(self, item: Any) -> None:
        try:
            result = await self.process(item)
            if result is not None and self.output_queue is not None:
                await self.output_queue.put(result)
        except Exception:
            traceback.print_exc()
        finally:
            self.input_queue.task_done()
            self.semaphore.release() # Release slot in the pool

    async def run(self) -> None:
        while True:
            # Shutdown Logic:
            # Stop ONLY if signal is set, queue is empty, AND no tasks are active
            if self.stop_signal.is_set() and self.input_queue.empty() and len(self.active_tasks) == 0:
                if self.next_stage_signal:
                    self.next_stage_signal.set()
                break

            self.active_tasks = {t for t in self.active_tasks if not t.done()}

            try:
                await self.semaphore.acquire()

                try:
                    item: Any = await asyncio.wait_for(self.input_queue.get(), timeout=0.1)
                except asyncio.TimeoutError:
                    self.semaphore.release() # We didn't get an item, release the slot
                    continue

                task = asyncio.create_task(self._process_wrapper(item))
                self.active_tasks.add(task)

            except Exception:
                traceback.print_exc()
                continue
