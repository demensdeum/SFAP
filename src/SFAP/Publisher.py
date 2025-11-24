from abc import ABC, abstractmethod
from .publisher_item import PublisherItem

class Publisher(ABC):
    def __init__(self) -> None:
        print("Publisher init")

    @abstractmethod
    async def publish(self, items: list[PublisherItem]) -> None:
        print("Publisher -> publish")
