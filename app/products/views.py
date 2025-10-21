from flask import Blueprint


products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def products_list():
    return "This is the list of products."

@products_bp.route('/<int:product_id>')
def product_details(product_id):
    return f"<h1>Displaying details for Product ID: {product_id}</h1>"