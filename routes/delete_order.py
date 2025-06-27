from app import app
from flask_login import login_required, current_user
from models import Session, Order
from flask import abort, flash, redirect, url_for


@app.route("/order/delete/<int:order_id>", methods=["POST"])
@login_required
def delete_order(order_id):
    with Session() as session:
        order = session.get(Order, order_id)
        session.delete(order)
        session.commit()
        flash("Замовлення видалено", "success")
    return redirect(url_for("index"))
