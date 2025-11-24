from abc import ABC, abstractmethod
from .seeker_item import SeekerItem

class Seeker(ABC):
    def __init__(self) -> None:
        print("Seeker init")

    @abstractmethod
    async def fetch(self) -> list[SeekerItem]:
        print("Seeker -> fetch")
        return []
