from .publisher import Publisher
from .publisher_item import PublisherItem
from .terminal_publisher_item import TerminalPublisherItem

class TerminalPublisher(Publisher):
    def __init__(self) -> None:
        super().__init__()
        print("TerminalPublisher")

    def publish(self, items: list[PublisherItem]) -> None:
        for item in items:
            if isinstance(item, TerminalPublisherItem):
                print(item.terminalRepresentation())
