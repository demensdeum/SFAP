from SFAP import SeekerItem
import WeatherSeekerItem

class WeatherSeekerItem(SeekerItem):
    def __init__(self, temperature, unit) -> None:
        super().__init__(args)
        print(f"WeatherSeekerItem init: {temperature} -> {unit}")
