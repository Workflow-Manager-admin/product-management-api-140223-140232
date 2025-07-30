from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError

from app.schemas.product import ProductSchema
from app.services.product_service import ProductService

blp = Blueprint("Products", "products", url_prefix="/products", description="Product CRUD endpoints")

@blp.route("/")
class ProductsListAPI(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """
        Returns a list of all products.
        """
        products = ProductService.get_all_products()
        return ProductSchema(many=True).dump(products), 200

    # PUBLIC_INTERFACE
    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        """
        Creates a new product.
        """
        try:
            product = ProductService.create_product(product_data)
            return ProductSchema().dump(product)
        except ValidationError as err:
            abort(400, message="Validation error", errors=err.messages)

@blp.route("/<int:product_id>")
class ProductAPI(MethodView):
    # PUBLIC_INTERFACE
    def get(self, product_id):
        """
        Retrieves details of a single product by ID.
        """
        product = ProductService.get_product_by_id(product_id)
        if not product:
            abort(404, message="Product not found")
        return ProductSchema().dump(product)

    # PUBLIC_INTERFACE
    @blp.arguments(ProductSchema)
    @blp.response(200, ProductSchema)
    def put(self, product_data, product_id):
        """
        Updates a product by ID.
        """
        product = ProductService.update_product(product_id, product_data)
        if not product:
            abort(404, message="Product not found")
        return ProductSchema().dump(product)

    # PUBLIC_INTERFACE
    def delete(self, product_id):
        """
        Deletes a product by ID.
        """
        deleted = ProductService.delete_product(product_id)
        if not deleted:
            abort(404, message="Product not found")
        return {"message": "Product deleted successfully"}, 200
