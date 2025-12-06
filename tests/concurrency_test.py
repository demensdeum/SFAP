import asyncio
import time
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from SFAP import Processor, Seeker, Filter, Adapter, Publisher, SeekerItem
import SFAP
print(f"SFAP location: {SFAP.__file__}")

class TestItem(SeekerItem):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

class MockSeeker(Seeker):
    def __init__(self, count: int):
        super().__init__()
        self.count = count

    async def read(self):
        for i in range(self.count):
            if self.output_queue:
                await self.output_queue.put(TestItem(i))

class SlowFilter(Filter):
    async def process(self, item):
        await asyncio.sleep(0.1) # Simulate work
        return item

class MockAdapter(Adapter):
    async def process(self, item):
        return item

class MockPublisher(Publisher):
    async def process(self, item):
        pass

async def run_test(concurrency: int, count: int):
    seeker = MockSeeker(count)
    filter = SlowFilter(concurrency=concurrency)
    adapter = MockAdapter()
    publisher = MockPublisher()
    
    start_time = time.time()
    await Processor(seeker, filter, adapter, publisher).start()
    end_time = time.time()
    
    return end_time - start_time

async def main():
    count = 10
    
    print(f"Running with concurrency=1, items={count}...")
    time_1 = await run_test(1, count)
    print(f"Time taken: {time_1:.2f}s")
    
    print(f"Running with concurrency=5, items={count}...")
    time_5 = await run_test(5, count)
    print(f"Time taken: {time_5:.2f}s")
    
    if time_5 < time_1 * 0.5:
        print("SUCCESS: Parallel execution is significantly faster.")
    else:
        print("FAILURE: Parallel execution is not significantly faster.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
