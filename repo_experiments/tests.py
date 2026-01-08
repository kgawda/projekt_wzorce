from dataclasses import dataclass
from service_layer import InMemoryUnitOfWork, MessageBus
from repos import InMemoryRepo
from model import Message, Product, OutOfStock

def test_get_product():
    repo = InMemoryRepo()
    product = Product(sku="1", quantity=5)

    repo.save(product)
    product_got = repo.get(product.sku)

    assert product_got == product

def test_seen_on_read():
    repo = InMemoryRepo()
    repo._data["1"] = Product(sku="1", quantity=5)

    repo.get("1")

    assert len(repo.seen) == 1
    assert repo.seen[0].quantity == 5

def test_seen_on_save():
    repo = InMemoryRepo()
    product = Product(sku="1", quantity=5)
    repo.save(product)

    assert len(repo.seen) == 1
    assert repo.seen[0].quantity == 5

def test_overbooked():
    product = Product(sku="1", quantity=5)
    product.allocate(10)
    assert len(product.messages) == 1
    assert product.messages[0] == OutOfStock("1")

def test_uow_transaction():
    with InMemoryUnitOfWork() as uow:
        repo = uow.products
        product = Product(sku="1", quantity=5)
        repo.save(product)

        saved_product = repo.get(product.sku)
        saved_product.allocate(10)
    
    messages = list(uow.consume_messages())
    assert len(messages) == 1
    assert messages[0].sku == saved_product.sku

    assert len(list(uow.consume_messages())) == 0


def test_message_bus_basic():
    uow = InMemoryUnitOfWork()
    repo = uow.products

    product = Product(sku="1", quantity=5)
    repo._data["1"] = product

    @dataclass
    class Allocate(Message):
        sku: str
        quantity: int

    def order_added_handler(msg: Allocate, uow):
        with uow:
            product = uow.products.get(msg.sku)
            product.allocate(msg.quantity)

    bus = MessageBus(uow=uow, handlers={Allocate: [order_added_handler]})
    bus.handle(Allocate("1", 1))

    assert repo.get("1").quantity == 4
    