import sys
import asyncio
from SFAP import Processor
from SFAP import PassthroughFilter
from SFAP import TerminalPublisher
from WeatherSeeker import WeatherSeeker
from WeatherTerminalPublisherAdapter import WeatherTerminalPublisherAdapter

URL_TO_SCRAPE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
delay = int(sys.argv[3])
HEADLESS = sys.argv[4] == "True"
CHUNK_SIZE = 3000
verbose = False

async def main():
    seeker = WeatherSeeker(
        URL_TO_SCRAPE,
        HEADLESS,
        delay,
        OUTPUT_FILE,
        CHUNK_SIZE,
        verbose=verbose
    )
    filter = PassthroughFilter()
    adapter = WeatherTerminalPublisherAdapter()
    publisher = TerminalPublisher()

    await Processor(seeker, filter, adapter, publisher).start()

if __name__ == "__main__":
    asyncio.run(main())
