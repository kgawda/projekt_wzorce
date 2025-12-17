from dataclasses import dataclass
from service_layer import InMemoryUnitOfWork, MessageBus
from repos import InMemoryRepo
from model import Message, Product, ProductOverbooked

def test_get_product():
    repo = InMemoryRepo()
    product = Product(id="1", name="Chair", quantity=5, orders=[])

    repo.save(product)
    product_got = repo.get(product.id)

    assert product_got == product

def test_seen_on_read():
    repo = InMemoryRepo()
    repo._data["1"] = Product(id="1", name="Chair", quantity=5, orders=[])

    repo.get("1")

    assert len(repo.seen) == 1
    assert repo.seen[0].name == "Chair"

def test_seen_on_save():
    repo = InMemoryRepo()
    product = Product(id="1", name="Chair", quantity=5, orders=[])
    repo.save(product)

    assert len(repo.seen) == 1
    assert repo.seen[0].name == "Chair"

def test_overbooked():
    product = Product(id="1", name="Chair", quantity=5, orders=[])
    product.add_new_order(10)
    assert len(product.messages) == 1
    assert product.messages[0] == ProductOverbooked("1")

def test_uow_transaction():
    repo = InMemoryRepo()
    with InMemoryUnitOfWork(repo) as uow:
        product = Product(id="1", name="Chair", quantity=5, orders=[])
        repo.save(product)

        saved_product = repo.get(product.id)
        saved_product.add_new_order(10)
    
    messages = list(uow.consume_messages())
    assert len(messages) == 1
    assert messages[0].product_id == saved_product.id

    assert len(list(uow.consume_messages())) == 0


def message_bus_basic():
    repo = InMemoryRepo()
    uow = InMemoryUnitOfWork(repo)

    product = Product(id="1", name="Chair", quantity=5, orders=[])
    repo._data["1"] = product

    @dataclass
    class OrderAdded(Message):
        product_id: str
        quantity: int

    def order_added_handler(msg: OrderAdded, uow):
        with uow:
            product = uow.products.get(msg.product_id)
            product.add_new_order(msg.quantity)

    bus = MessageBus(uow=uow, handlers={OrderAdded: [order_added_handler]})
    bus.handle(OrderAdded("1", 1))

    assert repo.get("1").orders == [1]
    