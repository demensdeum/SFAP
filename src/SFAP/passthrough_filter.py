from .async_items_handler import AsyncItemsHandler
from typing import Any

class PassthroughFilter(AsyncItemsHandler):
    def __init__(self) -> None:
        super().__init__()

    async def process(self, item: Any) -> Any:
        return item
