from flask import Blueprint, render_template
from flask_login import login_required

from models.product import Product

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)


@products_bp.route("/")

def index():

    products = Product.query.order_by(
        Product.display_name.asc()
    ).all()

    return render_template(
        "products/index.html",
        products=products
    )