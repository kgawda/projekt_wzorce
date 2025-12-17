from repos import InMemoryRepo
from model import Product

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