import asyncio
import sys
import os
import random

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from SFAP import Processor, Seeker, Filter, Adapter, Publisher, SeekerItem, PassthroughFilter, TerminalPublisher
from typing import Any

class TestItem(SeekerItem):
    def __init__(self, value: str):
        super().__init__()
        self.value = value
    
    def __repr__(self):
        return f"TestItem({self.value})"

class MockSeeker(Seeker):
    def __init__(self, name: str, count: int):
        super().__init__()
        self.name = name
        self.count = count

    async def read(self):
        for i in range(self.count):
            await asyncio.sleep(random.uniform(0.01, 0.05))
            if self.output_queue:
                await self.output_queue.put(TestItem(f"{self.name}-{i}"))

class TaggingFilter(PassthroughFilter):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    async def process(self, item: Any) -> Any:
        item.value += f"->{self.name}"
        await asyncio.sleep(random.uniform(0.01, 0.05))
        return item

class TaggingAdapter(Adapter):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    async def process(self, item: Any) -> Any:
        item.value += f"->{self.name}"
        await asyncio.sleep(random.uniform(0.01, 0.05))
        return item

class CollectingPublisher(Publisher):
    def __init__(self):
        super().__init__()
        self.items = []

    async def process(self, item):
        self.items.append(item)
        return item

async def main():
    seeker1 = MockSeeker("S1", 5)
    seeker2 = MockSeeker("S2", 5)
    
    filter1 = TaggingFilter("F1")
    filter2 = TaggingFilter("F2")
    
    adapter1 = TaggingAdapter("A1")
    adapter2 = TaggingAdapter("A2")
    
    publisher = CollectingPublisher()
    
    print("Starting Processor with full parallelism...")
    await Processor(
        [seeker1, seeker2],
        [filter1, filter2],
        [adapter1, adapter2],
        publisher
    ).start()
    
    print(f"Collected {len(publisher.items)} items.")
    
    expected_count = 10
    if len(publisher.items) == expected_count:
        print("SUCCESS: Received all items.")
        for item in publisher.items:
            print(f"Item: {item.value}")
            # Verify path
            if "->F" not in item.value or "->A" not in item.value:
                 print(f"FAILURE: Item {item} did not pass through filter/adapter correctly.")
                 sys.exit(1)
    else:
        print(f"FAILURE: Expected {expected_count} items, got {len(publisher.items)}.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
