from SFAP.SeekerInput import SeekerInput
from SFAP.Seeker import Seeker
from SFAP.Filter import Filter
from SFAP.Publisher import Publisher

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
