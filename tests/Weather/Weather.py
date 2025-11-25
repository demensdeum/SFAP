import sys
import asyncio
from SFAP import Processor
from WeatherFilter import WeatherFilter
from SFAP import TerminalPublisher
from WeatherSeeker import WeatherSeeker
from WeatherTerminalPublisherAdapter import WeatherTerminalPublisherAdapter

URL_TO_SCRAPE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
delay = int(sys.argv[3])
HEADLESS = sys.argv[4] == "True"
verbose = False

async def main():
    seeker = WeatherSeeker(
        URL_TO_SCRAPE,
        HEADLESS,
        delay,
        OUTPUT_FILE,
        verbose=verbose
    )
    filter = WeatherFilter(3000, verbose)
    adapter = WeatherTerminalPublisherAdapter()
    publisher = TerminalPublisher()

    await Processor(seeker, filter, adapter, publisher).start()

if __name__ == "__main__":
    asyncio.run(main())
