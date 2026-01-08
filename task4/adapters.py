from collections.abc import Iterable
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, event
from sqlalchemy.orm import registry, sessionmaker, Session
from model import Product
from service_layer import AbstractUnitOfWork # Zakładamy, że AbstractUoW jest w service_layer (lub oddzielnym pliku interface'ów)

# --- ORM Config (Pure DDD style) ---
mapper_registry = registry()
metadata = MetaData()
products_table = Table(
    "products",
    metadata,
    Column("sku", String(255), primary_key=True),
    Column("quantity", Integer, nullable=False),
)

def start_mappers():
    # Mapuje klasę Product na tabelę products bez dotykania kodu klasy
    mapper_registry.map_imperatively(Product, products_table)

# --- Repository Implementation ---
class SqlAlchemyRepository:
    def __init__(self, session: Session):
        self.session = session
        self.seen: list[Product] = []

    def add(self, product: Product):
        self._add(product)
        self.seen.append(product)

    def get(self, sku: str) -> Product | None:
        product = self._get(sku)
        if product:
            self.seen.append(product)
        return product

    def list(self) -> Iterable[Product]:
        result = []
        for product in self.session.query(Product).all():
            self.seen.append(product)
            result.append(product)
        return result

    def _add(self, product):
        self.session.add(product)

    def _get(self, sku):
        return self.session.query(Product).filter_by(sku=sku).first()

@event.listens_for(Product, 'load')
def receive_load(product, _):
    product.messages = []

# --- Unit of Work Implementation ---
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine("sqlite:///inventory.db", connect_args={"check_same_thread": False})
)

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.products = SqlAlchemyRepository(self.session)
        return self

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

# Helper do inicjalizacji bazy przy starcie
def create_tables():
    engine = DEFAULT_SESSION_FACTORY.kw['bind']
    metadata.create_all(engine)