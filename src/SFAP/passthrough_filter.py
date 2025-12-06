from .filter import Filter
from typing import Any

class PassthroughFilter(Filter):
    def __init__(self, concurrency: int = 1) -> None:
        super().__init__(concurrency)

    async def process(self, item: Any) -> Any:
        return item
