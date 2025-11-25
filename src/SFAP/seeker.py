import asyncio
import random
from typing import Optional, Any, Dict
from .async_items_handler import AsyncItemsHandler
from .seeker_item import SeekerItem

class Seeker:
    output_queue: Optional[asyncio.Queue[Any]]
    next_stage_signal: Optional[asyncio.Event]

    def __init__(self) -> None:
        self.output_queue = None
        self.next_stage_signal = None

    def link(self, next_stage: Any) -> Any:
        self.output_queue = next_stage.input_queue
        self.next_stage_signal = next_stage.stop_signal
        return next_stage

    async def read(self) -> None:
        raise NotImplementedError

    async def run(self) -> None:
        await self.read()

        if self.next_stage_signal:
            self.next_stage_signal.set()
