
from abc import ABC, abstractmethod
import copy


class Drawer(ABC):
    supported_extensions: list[str]

    @abstractmethod
    def draw(self, svg_data: str, add_frame: bool) -> None:
        ...

class TrivialDrawer(Drawer):
    def draw(self, svg_data: str, add_frame: bool) -> None:
        print(svg_data)


class BuildingDesign:
    drawings: list[str|bytes]|None = None
    drawer: Drawer

    def __init__(self, drawer: Drawer) -> None:
        self.drawer = drawer

    def copy(self):
        new = BuildingDesign(drawer=self.drawer)
        if self.drawings is not None:
            new.drawings = self.drawings.copy()
        return new


if __name__ == "__main__":
    design = BuildingDesign(TrivialDrawer())
    copy1 = design.copy()
    copy2 = copy.deepcopy(design)