class SVG:
    def __init__(self, height: int, width: int) -> None:
        self._height = height
        self._width = width

    def render(self) -> str:
        return f'<svg viewBox="0 0 {self._width} {self._height}"></svg>'
