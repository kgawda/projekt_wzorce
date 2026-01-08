from abc import ABC
from dataclasses import dataclass, field

@dataclass
class Message(ABC):
    pass

@dataclass
class OutOfStock(Message):
    sku: str


@dataclass
class Product:
    sku: str            # Stock Keeping Unit (ID)
    quantity: int       # Dostępna ilość
    messages: list[Message] = field(default_factory=list)

    def can_allocate(self, amount: int) -> bool:
        return self.quantity >= amount

    def allocate(self, amount: int) -> None:
        if self.can_allocate(amount):
            self.quantity -= amount
        else:
            # Domain Event: Próbowano zamówić, ale brak towaru
            self.messages.append(OutOfStock(self.sku))

    def restock(self, amount: int) -> None:
        self.quantity += amount