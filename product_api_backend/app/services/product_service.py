from app.models.product import Product
from app.database import SessionLocal

# PUBLIC_INTERFACE
class ProductService:
    """
    Service layer for handling product business logic and interaction with the database.
    """

    @staticmethod
    def get_all_products():
        session = SessionLocal()
        try:
            products = session.query(Product).all()
            return products
        finally:
            session.close()

    @staticmethod
    def get_product_by_id(product_id):
        session = SessionLocal()
        try:
            product = session.query(Product).filter_by(id=product_id).one_or_none()
            return product
        finally:
            session.close()

    @staticmethod
    def create_product(data):
        session = SessionLocal()
        try:
            product = Product(**data)
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
        finally:
            session.close()

    @staticmethod
    def update_product(product_id, data):
        session = SessionLocal()
        try:
            product = session.query(Product).filter_by(id=product_id).one_or_none()
            if not product:
                return None
            for key, value in data.items():
                setattr(product, key, value)
            session.commit()
            session.refresh(product)
            return product
        finally:
            session.close()

    @staticmethod
    def delete_product(product_id):
        session = SessionLocal()
        try:
            product = session.query(Product).filter_by(id=product_id).one_or_none()
            if not product:
                return False
            session.delete(product)
            session.commit()
            return True
        finally:
            session.close()
