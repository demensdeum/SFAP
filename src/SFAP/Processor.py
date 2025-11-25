from .seeker_input import SeekerInput
from .seeker import Seeker
from .filter import Filter
from .publisher import Publisher
from .adapter import Adapter
import asyncio

class Processor:
    def __init__(
        self,
        seeker: Seeker,
        filter: Filter,
        adapter: Adapter,
        publisher: Publisher
    ) -> None:
        self.seeker = seeker
        self.filter = filter
        self.adapter = adapter
        self.publisher = publisher

    async def start(self) -> None:
        self.seeker.link(self.filter).link(self.adapter).link(self.publisher)

        await asyncio.gather(
            self.seeker.run(),
            self.filter.run(),
            self.adapter.run(),
            self.publisher.run()
        )
