
from abc import ABC, abstractmethod
import copy
import requests


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


class SiteChecker:
    session: requests.Session

    def __init__(self) -> None:
        self.session = requests.Session()
        
    def check_http(self, domain: str):
        try:
            response = requests.get(f"http://{domain}")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


if __name__ == "__main__":
    design = BuildingDesign(TrivialDrawer())
    copy1 = design.copy()
    copy2 = copy.deepcopy(design)
    
    checker = SiteChecker()
    for domain in ["example.com",]:
        if checker.check_http(domain):
            print(f"Domain {domain} works")
