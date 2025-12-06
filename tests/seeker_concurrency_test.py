import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from SFAP import Processor, Seeker, Filter, Adapter, Publisher, SeekerItem, PassthroughFilter, TerminalPublisher

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
            await asyncio.sleep(0.1) # Simulate work
            if self.output_queue:
                await self.output_queue.put(TestItem(f"{self.name}-{i}"))

class CollectingPublisher(Publisher):
    def __init__(self):
        super().__init__()
        self.items = []

    async def process(self, item):
        self.items.append(item)
        return item

class MockAdapter(Adapter):
    async def process(self, item):
        return item

async def main():
    seeker1 = MockSeeker("S1", 5)
    seeker2 = MockSeeker("S2", 5)
    
    filter = PassthroughFilter()
    adapter = MockAdapter()
    publisher = CollectingPublisher()
    
    print("Starting Processor with 2 concurrent Seekers...")
    await Processor([seeker1, seeker2], filter, adapter, publisher).start()
    
    print(f"Collected {len(publisher.items)} items.")
    
    expected_count = 10
    if len(publisher.items) == expected_count:
        print("SUCCESS: Received all items from both seekers.")
    else:
        print(f"FAILURE: Expected {expected_count} items, got {len(publisher.items)}.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
