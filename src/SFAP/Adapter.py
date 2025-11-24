from abc import ABC, abstractmethod

class Adapter(ABC):
    def __init__(self):
        print("Adapter init")

    @abstractmethod
    async def adapt(self):
        print("Adapter -> adapt")
