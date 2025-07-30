from flask import jsonify
from marshmallow import ValidationError

# PUBLIC_INTERFACE
def register_error_handlers(app):
    """
    Registers custom error handlers for the Flask app.
    """
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation_error(e):
        return jsonify({"code": 400, "status": "Bad Request", "message": str(e), "errors": e.messages}), 400

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"code": 404, "status": "Not Found", "message": "Resource not found"}), 404

    @app.errorhandler(400)
    def handle_400(e):
        return jsonify({"code": 400, "status": "Bad Request", "message": str(e)}), 400

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"code": 500, "status": "Internal Server Error", "message": "An internal error occurred"}), 500
