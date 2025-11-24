from abc import ABC, abstractmethod

class Publisher(ABC):
    def __init__(self):
        print("Publisher init")

    @abstractmethod
    async def publish(self):
        print("Publisher -> publish")
