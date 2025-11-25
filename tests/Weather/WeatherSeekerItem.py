from SFAP import SeekerItem
import WeatherSeekerItem

class WeatherSeekerItem(SeekerItem):
    def __init__(self, temperature: str) -> None:
        super().__init__()
        self.temperature = temperature
