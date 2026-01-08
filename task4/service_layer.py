from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Callable, Self

from repos import InMemoryRepo, Repository
from model import Message, OutOfStock


class AbstractUnitOfWork(ABC):
    products: Repository

    # __init__ creates .products repository. May need some session factory as an argument

    def __enter__(self) -> Self:
        return self

    def __exit__(self, type_, value, traceback) -> bool:
        if type_ is None:
            self.commit()
        else:
            self.rollback()
        return False
    
    def consume_messages(self) -> Iterator[Message]:
        for s in self.products.seen:
            while s.messages:
                yield s.messages.pop()

    @abstractmethod
    def commit(self): ...

    @abstractmethod
    def rollback(self): ...



# --- Messages Definitions ---
@dataclass
class Allocate(Message):
    sku: str
    amount: int

@dataclass
class CreateProduct(Message):
    sku: str
    qty: int


class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self.products = InMemoryRepo()

    def commit(self):
        pass  # może warto coś zapisać jako informację dla testów

    def rollback(self):
        pass


class MessageBus:
    def __init__(self, handlers: dict[type, list[Callable]], uow: AbstractUnitOfWork):
        self.handlers = handlers
        self.uow = uow
        self.queue: list[Message] = []

    def handle(self, message: Message):
        self.queue.append(message)
        
        while self.queue:
            current_msg = self.queue.pop(0)
            msg_type = type(current_msg)
            
            for handler in self.handlers.get(msg_type, ()):
                handler(current_msg, self.uow)
            self.queue.extend(self.uow.consume_messages())



# --- ZADANIE 1: Zaimplementować Handlery ---

def allocate_handler(cmd: Allocate, uow: AbstractUnitOfWork):
    """
    1. Użyj uow jako context managera.
    2. Pobierz produkt z repozytorium (uow.products.get).
    3. Wywołaj metodę domeny (product.allocate).
    """
    pass  # TODO

def create_product_handler(cmd: CreateProduct, uow: AbstractUnitOfWork):
    """
    1. Utwórz nowy obiekt Product.
    2. Dodaj go do repozytorium (uow.products.add).
    """
    pass  # TODO


def out_of_stock_handler(event, uow):
    print(f"ALARM: Brak towaru w magazynie dla SKU: {event.sku}!")


HANDLERS = {
    Allocate: [allocate_handler],
    CreateProduct: [create_product_handler],
    OutOfStock: [out_of_stock_handler],
}