from abc import ABC, abstractmethod

class Filter(ABC):
    def __init__(self):
        print("Filter init")

    @abstractmethod
    async def filter(self, job):
        print("Filter -> filter")
