import sys
import WeatherSeeker
import asyncio

URL_TO_SCRAPE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
delay = int(sys.argv[3])
HEADLESS = sys.argv[4] == "True"
CHUNK_SIZE = 3000

async def main():
    weather_seeker = WeatherSeeker.WeatherSeeker(
        URL_TO_SCRAPE,
        HEADLESS,
        delay,
        OUTPUT_FILE,
        CHUNK_SIZE,
        verbose=False
    )
    weather_seeker.seek()

if __name__ == "__main__":
    asyncio.run(main())
