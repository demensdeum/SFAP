import asyncio
from typing import List
from bs4 import BeautifulSoup
from pydantic import BaseModel
from SFAP import Filter, TerminalPublisherItem
from ollama_call import ollama_call
from WeatherSeekerItem import WeatherSeekerItem
from typing import Any

class TemperatureResponse(BaseModel):
    temperatures: List[str]

class WeatherFilter(Filter):
    def __init__(self, chunk_size:int, verbose: bool) -> None:
        super().__init__()
        self.chunk_size = chunk_size
        self.verbose = verbose

    async def process(self, item: Any) -> Any:
        if self.verbose:
            print(f"Filter processing HTML from: {item.source_url}")

        temperature_response = await asyncio.to_thread(
            self.ollama_parse_temperature, item.html_content, self.verbose
        )

        if temperature_response and len(temperature_response.temperatures) > 0:
            found_temp = temperature_response.temperatures[0]
            if self.verbose:
                print(f"Filter found temperature: {found_temp}")
            return WeatherSeekerItem(f"Temperature: {found_temp}")
        else:
            return WeatherSeekerItem("Temperature not found in source.")

    def get_html_chunks(self, html_content: Any, chunk_size: int) -> Any:
        soup = BeautifulSoup(html_content, 'html.parser')

        for redundant in soup(["script", "style", "svg", "path", "head", "meta", "noscript"]):
            redundant.decompose()

        clean_text = soup.get_text(separator="\n", strip=True)

        for i in range(0, len(clean_text), chunk_size):
            yield clean_text[i:i + chunk_size]

    def ollama_parse_temperature(self, html_content: Any, verbose: bool) -> Any:
        if not html_content:
            return None

        if verbose:
            print("Processing HTML in chunks...")

        chunk_counter = 1
        for chunk in self.get_html_chunks(html_content, self.chunk_size):
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
                format=TemperatureResponse.model_json_schema(), # type: ignore[attr-defined]
                verbose=verbose
            )

            if verbose:
                print(f"Raw Ollama Response: {response_str}")

            try:
                result = TemperatureResponse.model_validate_json(response_str) # type: ignore[attr-defined]
                if result.temperatures:
                    return result
            except Exception as e:
                print(f"Validation Error: {e}")

            chunk_counter += 1

        print("\n❌ No temperature data found.")
        return TemperatureResponse(temperatures=[])
