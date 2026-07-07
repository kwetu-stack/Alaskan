from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)

from config import now_in_nairobi
from models import db
from models.product import Product
from models.receipt import Receipt
from models.receipt_item import ReceiptItem

receipts_bp = Blueprint("receipts", __name__, url_prefix="/receipts")
DEFAULT_RECEIPT_CUSTOMER_NAME = "MABROUK SHOP ALASKAN"


# ----------------------------
# MAIN SCREEN
# ----------------------------
@receipts_bp.route("/new", methods=["GET"])
def new_receipt():

    receipt = None
    receipt_id = session.get("receipt_id")

    if receipt_id is not None:
        receipt = db.session.get(Receipt, receipt_id)

    if receipt is None:
        receipt = Receipt(
            receipt_number=f"R{now_in_nairobi().strftime('%Y%m%d%H%M%S')}",
            customer_name="",
            created_by=1,
            total_amount=0,
            status="OPEN",
        )

        db.session.add(receipt)
        db.session.commit()
        session["receipt_id"] = receipt.id

    products = Product.query.order_by(Product.display_name).all()

    items = ReceiptItem.query.filter_by(receipt_id=receipt.id).all()

    total = sum(item.total for item in items)

    return render_template(
        "receipts/new.html",
        receipt=receipt,
        products=products,
        items=items,
        total=total,
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
        total=total,
    )

    db.session.add(item)
    db.session.commit()

    # Update receipt total
    receipt = Receipt.query.get(receipt_id)

    receipt.total_amount = sum(i.total for i in receipt.items)

    db.session.commit()

    return redirect(url_for("receipts.new_receipt"))


@receipts_bp.route("/api/add-item", methods=["POST"])
def api_add_item():

    if "receipt_id" not in session:
        return jsonify({"error": "No active receipt"}), 400

    receipt_id = session["receipt_id"]
    data = request.get_json()

    customer_name = data.get("customer_name", "Walk-in Customer")

    product_id = int(data["product_id"])
    quantity = float(data["quantity"])
    unit_price = float(data["unit_price"])

    total = quantity * unit_price

    item = ReceiptItem(
        receipt_id=receipt_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        total=total,
    )

    db.session.add(item)
    db.session.commit()

    receipt = Receipt.query.get(receipt_id)
    receipt.customer_name = customer_name

    receipt.total_amount = sum(i.total for i in receipt.items)

    db.session.commit()

    return jsonify(
        {
            "success": True,
            "item": {
                "id": item.id,
                "product": item.product.display_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.total,
            },
            "grand_total": receipt.total_amount,
        }
    )


# ----------------------------
# SAVE RECEIPT
# ----------------------------
@receipts_bp.route("/save", methods=["POST"])
def save_receipt():

    if "receipt_id" not in session:
        return redirect(url_for("receipts.new_receipt"))

    receipt = Receipt.query.get(session["receipt_id"])

    # Update customer name
    receipt.customer_name = request.form.get("customer_name", "Walk-in Customer")

    # Calculate final total
    receipt.total_amount = sum(item.total for item in receipt.items)

    # Close receipt
    receipt.status = "SAVED"

    db.session.commit()

    # Receipt finished
    session.pop("receipt_id", None)

    return redirect(url_for("receipts.view_receipt", receipt_id=receipt.id))


# ----------------------------
# VIEW RECEIPT
# ----------------------------
@receipts_bp.route("/view/<int:receipt_id>")
def view_receipt(receipt_id):

    receipt = Receipt.query.get_or_404(receipt_id)

    items = ReceiptItem.query.filter_by(receipt_id=receipt.id).all()

    return render_template("receipts/view.html", receipt=receipt, items=items)


@receipts_bp.route("/print/<int:receipt_id>")
def print_receipt(receipt_id):

    receipt = Receipt.query.get_or_404(receipt_id)

    items = ReceiptItem.query.filter_by(receipt_id=receipt.id).all()

    return render_template("receipts/print.html", receipt=receipt, items=items)
