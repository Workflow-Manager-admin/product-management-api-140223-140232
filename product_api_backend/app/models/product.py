from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# PUBLIC_INTERFACE
class Product(Base):
    """
    Product model representing a product in the database.
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(256), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
