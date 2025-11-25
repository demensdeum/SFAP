from SFAP import Adapter
from SFAP import TerminalPublisherItem

class WeatherTerminalPublisherAdapter(Adapter):
    def __init__(self):
        super().__init__()

    async def process(self, item):
        output = TerminalPublisherItem(f"Temperature: {item.temperature}")
        return output
