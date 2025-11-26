import asyncio
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from SFAP import Seeker
from dataclasses import dataclass
from typing import Any

@dataclass
class WeatherRawHtmlItem:
    html_content: str
    source_url: str

class WeatherSeeker(Seeker):
    def __init__(
        self,
        URL_TO_SCRAPE: str,
        HEADLESS: bool,
        delay: float,
        OUTPUT_FILE: str,
        verbose: bool
    ) -> None:
        super().__init__()
        self.URL_TO_SCRAPE = URL_TO_SCRAPE
        self.HEADLESS = HEADLESS
        self.delay = delay
        self.OUTPUT_FILE = OUTPUT_FILE
        self.verbose = verbose

    async def read(self) -> None:
        if self.verbose:
            print(f"Seeker starting read for {self.URL_TO_SCRAPE}")

        html_content = await asyncio.to_thread(self.save_rendered_html)

        if html_content:
            item = WeatherRawHtmlItem(
                html_content=html_content,
                source_url=self.URL_TO_SCRAPE
            )

            if self.output_queue:
                await self.output_queue.put(item)
                if self.verbose:
                    print(f"Queued raw HTML item for processing.")
        else:
            if self.verbose:
                print("Failed to retrieve HTML content.")

    def save_rendered_html(self) -> Any:
        chrome_options = Options()
        if self.HEADLESS:
            chrome_options.add_argument("--headless")

        if self.verbose:
            print(f"HEADLESS: {self.HEADLESS}")

        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        if self.verbose:
            print("Initializing Browser...")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        html_content = ""
        try:
            if self.verbose:
                print(f"Loading: {self.URL_TO_SCRAPE}")
            driver.get(self.URL_TO_SCRAPE)

            if self.verbose:
                print(f"Waiting {self.delay} seconds for JS to finish...")
            time.sleep(self.delay)

            html_content = driver.page_source

            with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(html_content)

            if self.verbose:
                print(f"Success! Saved locally to {self.OUTPUT_FILE}")

        except Exception as e:
            print(f"An error occurred during scraping: {e}")

        finally:
            driver.quit()

        return html_content
