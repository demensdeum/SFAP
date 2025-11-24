from abc import ABC, abstractmethod

class SeekerItem(ABC):
    def __init__(self) -> None:
        print("SeekerItem init")
