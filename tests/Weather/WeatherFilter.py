from SFAP import Filter

class WeatherFilter(Filter):
    def __init__(self):
        super().__init__()

    async def process(self, item):
        return TerminalPublisherItem(f"Temperature: {item.temperature}")
