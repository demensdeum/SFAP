import sys
import time
from ollama_call import ollama_call
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List

URL_TO_SCRAPE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
delay = int(sys.argv[3])
HEADLESS = True
CHUNK_SIZE = 3000

class TemperatureResponse(BaseModel):
    temperatures: List[str]

def get_html_chunks(html_content, chunk_size):
    soup = BeautifulSoup(html_content, 'html.parser')

    for redundant in soup(["script", "style", "svg", "path", "head", "meta", "noscript"]):
        redundant.decompose()

    clean_text = soup.get_text(separator="\n", strip=True)

    for i in range(0, len(clean_text), chunk_size):
        yield clean_text[i:i + chunk_size]

def save_rendered_html():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    print("Initializing Browser...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print(f"Loading: {URL_TO_SCRAPE}")
        driver.get(URL_TO_SCRAPE)

        print(f"Waiting {delay} seconds for JS to finish...")
        time.sleep(delay)

        html_content = driver.page_source

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Success! Saved to {OUTPUT_FILE}")

        return html_content

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

def ollama_parse_temperature(html_content):
    if not html_content:
        return

    print("Processing HTML in chunks...")

    chunk_counter = 1
    for chunk in get_html_chunks(html_content, CHUNK_SIZE):
        print(f"--- Analyzing Chunk {chunk_counter} ---")

        prompt = (
            f"Analyze the following text extracted from a webpage:\n"
            f"\"{chunk}\"\n\n"
            f"Task: Find the temperature in Celsius (°C) or Fahrenheit (°F).\n"
            f"Rules:\n"
            f"1. Extract the values exactly as they appear in text.\n"
            f"2. Do NOT convert the values yourself. Only report what is written.\n"
            f"3. Output format: 'Temperature: <value>'.\n"
            f"4. If NO temperature data is found at all, output exactly 'NOT_FOUND'."
        )

        response_str = ollama_call(
            prompt,
            format=TemperatureResponse.model_json_schema()
        )

        print(f"Raw Ollama Response: {response_str}")

        try:
            result = TemperatureResponse.model_validate_json(response_str)

            if result.temperatures:
                print(f"\n✅ Temperatures Found: {result.temperatures}")
                return result.model_dump()

        except Exception as e:
            print(f"Validation Error: {e}")

        chunk_counter += 1

    print("\n❌ No temperature data found.")
    return {"temperatures": []}

if __name__ == "__main__":
    html_content = save_rendered_html()
    ollama_parse_temperature(html_content)
