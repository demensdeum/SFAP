from abc import ABC, abstractmethod

class Adapter(ABC):
    def __init__(self) -> None:
        print("Adapter init")

    @abstractmethod
    async def adapt(self) -> None:
        print("Adapter -> adapt")
