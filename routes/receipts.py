from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from models import db
from models.product import Product
from models.receipt import Receipt
from models.receipt_item import ReceiptItem


receipts_bp = Blueprint(
    "receipts",
    __name__,
    url_prefix="/receipts"
)


# ----------------------------
# MAIN SCREEN
# ----------------------------
@receipts_bp.route("/new", methods=["GET"])
def new_receipt():

    # Create receipt only once per session
    if "receipt_id" not in session:

        receipt = Receipt(
            receipt_number=f"R{datetime.now().strftime('%Y%m%d%H%M%S')}",
            customer_name="Walk-in Customer",
            created_by=1,
            total_amount=0,
            status="OPEN"
        )

        db.session.add(receipt)
        db.session.commit()

        session["receipt_id"] = receipt.id

    receipt = Receipt.query.get(session["receipt_id"])

    products = Product.query.order_by(
        Product.display_name
    ).all()

    items = ReceiptItem.query.filter_by(
        receipt_id=receipt.id
    ).all()

    total = sum(item.total for item in items)

    return render_template(
        "receipts/new.html",
        receipt=receipt,
        products=products,
        items=items,
        total=total
    )


# ----------------------------
# ADD ITEM (CORE LOGIC)
# ----------------------------
@receipts_bp.route("/add-item", methods=["POST"])
def add_item():

    if "receipt_id" not in session:
        return redirect(url_for("receipts.new_receipt"))

    receipt_id = session["receipt_id"]

    product_id = int(request.form["product_id"])
    quantity = float(request.form["quantity"])
    unit_price = float(request.form["unit_price"])

    total = quantity * unit_price

    item = ReceiptItem(
        receipt_id=receipt_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        total=total
    )

    db.session.add(item)
    db.session.commit()

    # Update receipt total
    receipt = Receipt.query.get(receipt_id)

    receipt.total_amount = sum(i.total for i in receipt.items)

    db.session.commit()

    return redirect(url_for("receipts.new_receipt"))
from flask import jsonify
@receipts_bp.route("/api/add-item", methods=["POST"])
def api_add_item():

    if "receipt_id" not in session:
        return jsonify({"error": "No active receipt"}), 400

    receipt_id = session["receipt_id"]

    data = request.get_json()

    product_id = int(data["product_id"])
    quantity = float(data["quantity"])
    unit_price = float(data["unit_price"])

    total = quantity * unit_price

    item = ReceiptItem(
        receipt_id=receipt_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        total=total
    )

    db.session.add(item)
    db.session.commit()

    receipt = Receipt.query.get(receipt_id)

    receipt.total_amount = sum(i.total for i in receipt.items)

    db.session.commit()

    return jsonify({
        "success": True,
        "item": {
            "id": item.id,
            "product": item.product.display_name,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total": item.total
        },
        "grand_total": receipt.total_amount
    })