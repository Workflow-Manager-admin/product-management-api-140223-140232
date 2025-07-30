from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class ProductSchema(Schema):
    """
    Product schema for serialization and deserialization.
    """
    id = fields.Int(dump_only=True, description="Product ID")
    name = fields.Str(required=True, validate=validate.Length(min=1, max=128), description="Product name")
    description = fields.Str(validate=validate.Length(max=256), allow_none=True, description="Product description")
    price = fields.Float(required=True, validate=validate.Range(min=0), description="Product price")
    quantity = fields.Int(required=True, validate=validate.Range(min=0), description="Product stock quantity")
