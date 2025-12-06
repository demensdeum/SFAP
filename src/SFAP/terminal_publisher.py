from .publisher import Publisher
from .publisher_item import PublisherItem
from .terminal_publisher_item import TerminalPublisherItem
from typing import Any

class TerminalPublisher(Publisher):
    def __init__(self, concurrency: int = 1) -> None:
        super().__init__(concurrency)

    async def process(self, item: Any) -> Any:
        if isinstance(item, TerminalPublisherItem):
            print(item.terminalRepresentation())
        else:
            print(f"Sorry can't publish non TerminalPublisherItem into terminal item: {item}")
        return item
