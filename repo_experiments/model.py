from abc import ABC
from dataclasses import dataclass, field

@dataclass
class Message(ABC):
    pass

@dataclass
class ProductOverbooked(Message):
    product_id: str


@dataclass
class Product:
    id: str
    name: str
    quantity: int
    orders: list[int] = field(default_factory=list)
    messages: list[Message] = field(default_factory=list)  # TODO: może by tak set zamiast list?

    def add_new_order(self, quantity: int) -> None:
        ordered = sum(self.orders)
        if self.quantity - ordered < quantity:
            self.messages.append(ProductOverbooked(self.id))
        self.orders.append(quantity)  # Pewnie dobrze by było przechowywać więcej informacji o zamowieniu niż quantity
