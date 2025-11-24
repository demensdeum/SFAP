from .seeker_input import SeekerInput
from .seeker import Seeker
from .filter import Filter
from .publisher import Publisher

class Processor:
    def __init__(
        self,
        seekers: list[Seeker],
        filters: list[Filter],
        publishers: list[Publisher]
    ) -> None:
        self.seekers = seekers
        self.filters = filters
        self.publishers = publishers

    def start(self) -> None:
        print("start")
