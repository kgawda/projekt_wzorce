from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any, Callable, Self

from repos import Repository
from model import Message


class AbstractUnitOfWork(ABC):
    products: Repository

    def __enter__(self) -> Self:
        return self

    def __exit__(self, type_, value, traceback) -> bool:
        if type_ is None:
            self.commit()
        else:
            self.rollback()
        return False
    
    @abstractmethod
    def consume_messages(self) -> Iterator[Message]: ...

    @abstractmethod
    def commit(self): ...

    @abstractmethod
    def rollback(self): ...


class InMemoryUnitOfWork(AbstractUnitOfWork):
    # TODO: lepiej żeby OuW tworzył repozytorium niż je dostawał.
    # I tak jest zależny od technologii DB (commit, rollback)
    # (ale za to będzie potrzebował dostać dane do utworzenia połączenia z DB)
    def __init__(self, products: Repository) -> None:
        self.products = products

    def consume_messages(self) -> Iterator[Message]:
        for s in self.products.seen:
            while s.messages:
                yield s.messages.pop()

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
