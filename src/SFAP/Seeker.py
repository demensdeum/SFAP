from abc import ABC, abstractmethod

class Seeker(ABC):
    def __init__(self):
        print("Seeker init")

    @abstractmethod
    async def fetch(self):
        print("Seeker -> fetch")
