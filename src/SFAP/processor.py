from .seeker_input import SeekerInput
from .seeker import Seeker
from .filter import Filter
from .publisher import Publisher
from .adapter import Adapter
import asyncio
from typing import Any

class Processor:
    def __init__(
        self,
        seeker: Seeker | list[Seeker],
        filter: Filter | list[Filter],
        adapter: Adapter | list[Adapter],
        publisher: Publisher | list[Publisher]
    ) -> None:
        self.seekers = seeker if isinstance(seeker, list) else [seeker]
        self.filters = filter if isinstance(filter, list) else [filter]
        self.adapters = adapter if isinstance(adapter, list) else [adapter]
        self.publishers = publisher if isinstance(publisher, list) else [publisher]

    def _prepare_stage(self, stage_items: list[Any], input_queue: asyncio.Queue, stop_signal: asyncio.Event) -> None:
        for item in stage_items:
            item.input_queue = input_queue
            item.stop_signal = stop_signal
            # We don't let the item signal the next stage directly
            item.next_stage_signal = None

    async def start(self) -> None:
        # Create shared queues/signals
        filter_queue: asyncio.Queue[Any] = asyncio.Queue()
        filter_stop = asyncio.Event()
        self._prepare_stage(self.filters, filter_queue, filter_stop)
        
        adapter_queue: asyncio.Queue[Any] = asyncio.Queue()
        adapter_stop = asyncio.Event()
        self._prepare_stage(self.adapters, adapter_queue, adapter_stop)
        
        publisher_queue: asyncio.Queue[Any] = asyncio.Queue()
        publisher_stop = asyncio.Event()
        self._prepare_stage(self.publishers, publisher_queue, publisher_stop)
        
        # Link outputs
        for s in self.seekers:
            s.output_queue = filter_queue
            s.next_stage_signal = None # Managed by processor
            
        for f in self.filters:
            f.output_queue = adapter_queue
            
        for a in self.adapters:
            a.output_queue = publisher_queue
            
        async def run_seekers() -> None:
            await asyncio.gather(*(s.run() for s in self.seekers))
            filter_stop.set()
            
        async def run_filters() -> None:
            await asyncio.gather(*(f.run() for f in self.filters))
            adapter_stop.set()
            
        async def run_adapters() -> None:
            await asyncio.gather(*(a.run() for a in self.adapters))
            publisher_stop.set()
            
        async def run_publishers() -> None:
            await asyncio.gather(*(p.run() for p in self.publishers))
            
        await asyncio.gather(
            run_seekers(),
            run_filters(),
            run_adapters(),
            run_publishers()
        )
