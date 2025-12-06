from .async_items_handler import AsyncItemsHandler

class Publisher(AsyncItemsHandler):
    def __init__(self, concurrency: int = 1) -> None:
        super().__init__(concurrency)
