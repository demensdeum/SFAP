from abc import ABC, abstractmethod

class Filter(ABC):
    def __init__(self) -> None:
        print("Filter init")

    @abstractmethod
    async def filter(self) -> None:
        print("Filter -> filter")
