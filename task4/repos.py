from abc import ABC, abstractmethod
from collections.abc import Iterable
from model import Product

class Repository(ABC):
    seen: list[Product]

    @abstractmethod
    def get(self, sku:str) -> Product: ...

    @abstractmethod
    def list(self) -> Iterable[Product]: ...

    @abstractmethod
    def save(self, product: Product) -> None: ...

class InMemoryRepo(Repository):
    def __init__(self) -> None:
        self._data = {}
        self.seen = []

    def get(self, sku:str) -> Product:
        product = self._data[sku]
        self.seen.append(product)  # można wyrzucić do Repository przy użyciu _get
        return product
    
    def list(self) -> Iterable[Product]:
        return list(self._data.values())

    def save(self, product: Product) -> None: 
        self.seen.append(product)  # można wyrzucić do Repository przy użyciu _save
        self._data[product.sku] = product
    