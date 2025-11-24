from SeekerInput import SeekerInput
from Seeker import Seeker
from Filter import Filter
from Publisher import Publisher

class Processor:
    def __init__(
        self,
        seekers: list[Seeker],
        filters: list[Filter],
        publishers: list[Publisher]
    ):
        self.seekers = seekers
        self.filters = filters
        self.publishers = publishers

    def start(self):
        print("start")
