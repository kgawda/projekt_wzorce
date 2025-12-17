from dataclasses import dataclass

@dataclass
class Product:
    id: str
    name: str
    quantity: int
    orders: list[int]

    def can_add_new_order(self, quantity: int) -> bool:
        ordered = sum(self.orders)
        return self.quantity - ordered >= quantity 
