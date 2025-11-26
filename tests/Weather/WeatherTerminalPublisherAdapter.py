from SFAP import Adapter
from SFAP import PublisherItem
from SFAP import TerminalPublisherItem
from typing import Any

class WeatherTerminalPublisherAdapter(Adapter):
    def __init__(self) -> None:
        super().__init__()

    async def process(self, item: Any) -> PublisherItem:
        output = TerminalPublisherItem(f"Temperature: {item.temperature}")
        return output
