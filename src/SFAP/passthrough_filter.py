from .filter import Filter
from typing import Any

class PassthroughFilter(Filter):
    def __init__(self) -> None:
        super().__init__()

    async def process(self, item: Any) -> Any:
        return item
