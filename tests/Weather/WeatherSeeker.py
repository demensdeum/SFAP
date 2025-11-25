import WeatherSeekerItem
import time
from ollama_call import ollama_call
from pydantic import BaseModel
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from SFAP import Seeker
from SFAP import TerminalPublisher
from SFAP import TerminalPublisherItem

class TemperatureResponse(BaseModel):
    temperatures: List[str]

class WeatherSeeker(Seeker):
    def __init__(
        self,
        URL_TO_SCRAPE,
        HEADLESS,
        delay,
        OUTPUT_FILE,
        CHUNK_SIZE,
        verbose=True
    ) -> None:
        self.URL_TO_SCRAPE=URL_TO_SCRAPE
        self.HEADLESS=HEADLESS
        self.delay=delay
        self.OUTPUT_FILE=OUTPUT_FILE
        self.CHUNK_SIZE = CHUNK_SIZE
        self.verbose=verbose

    def get_html_chunks(self, html_content, chunk_size):
        soup = BeautifulSoup(html_content, 'html.parser')

        for redundant in soup(["script", "style", "svg", "path", "head", "meta", "noscript"]):
            redundant.decompose()

        clean_text = soup.get_text(separator="\n", strip=True)

        for i in range(0, len(clean_text), chunk_size):
            yield clean_text[i:i + chunk_size]

    def save_rendered_html(self):
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
                print(f"Success! Saved to {self.OUTPUT_FILE}")

            return html_content

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()

    def ollama_parse_temperature(self, html_content, verbose=True):
        if not html_content:
            return

        if verbose:
            print("Processing HTML in chunks...")

        chunk_counter = 1
        for chunk in self.get_html_chunks(html_content, self.CHUNK_SIZE):
            if verbose:
                print(f"--- Analyzing Chunk {chunk_counter} ---")

            prompt = (
                f"Analyze the following text extracted from a webpage:\n"
                f"\"{chunk}\"\n\n"
                f"Task: Extract all temperature readings (Celsius or Fahrenheit) from the text.\n"
                f"Rules:\n"
                f"1. Extract the values exactly as they appear (e.g. '12°C', '72°F').\n"
                f"2. Do NOT convert values."
            )

            response_str = ollama_call(
                prompt,
                format=TemperatureResponse.model_json_schema(),
                verbose=verbose
            )

            if verbose:
                print(f"Raw Ollama Response: {response_str}")

            try:
                result = TemperatureResponse.model_validate_json(response_str)

                if len(result.temperatures) > 0:
                    TerminalPublisher().publish([TerminalPublisherItem(f"\n✅ Temperature Found: {result.temperatures[0]}")])

                    return result.model_dump()

            except Exception as e:
                print(f"Validation Error: {e}")

            chunk_counter += 1

        print("\n❌ No temperature data found.")
        return {"temperatures": []}

    def seek(self) -> list[WeatherSeekerItem]:
        html_content = self.save_rendered_html()
        self.ollama_parse_temperature(html_content, self.verbose)
        return []
