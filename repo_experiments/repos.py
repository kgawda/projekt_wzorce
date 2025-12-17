from abc import ABC, abstractmethod
from model import Product

class Repository(ABC):
    seen: list[Product]

    @abstractmethod
    def get(self, id:str) -> Product: ...

    @abstractmethod
    def save(self, product: Product) -> None: ...

class InMemoryRepo(Repository):
    def __init__(self) -> None:
        self._data = {}
        self.seen = []

    def get(self, id:str) -> Product:
        product = self._data[id]
        self.seen.append(product)  # można wyrzucić do Repository przy użyciu _get
        return product

    def save(self, product: Product) -> None: 
        self.seen.append(product)  # można wyrzucić do Repository przy użyciu _save
        self._data[product.id] = product
    