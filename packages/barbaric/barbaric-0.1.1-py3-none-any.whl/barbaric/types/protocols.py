from typing import Protocol


class Element(Protocol):
    def render(self) -> str:
        ...
