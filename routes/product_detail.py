from flask import request, redirect, url_for, flash, render_template
from models import Session, Asortiment, Order
from app import app, csrf
from flask_login import current_user, login_required
from datetime import datetime


@csrf.exempt
@app.route("/product/<int:product_id>", methods=["GET", "POST"])
@login_required
def product_detail(product_id):
    with Session() as session:
        product = session.get(Asortiment, product_id)

        if request.method == "POST":
            address = request.form.get("address")
            if not address:
                flash("Будь ласка, введіть адресу доставки")
                return render_template("product_detail.html", product=product)

            order = Order(
                user_id=current_user.id,
                order_time=datetime.utcnow(),
                status="pending",
                order_data={
                    "product_id": product.id,
                    "product_name": product.name,
                    "price": product.price,
                    "address": address,
                },
            )
            session.add(order)
            session.commit()

            flash(
                f"Дякуємо! Ваше замовлення буде доставлено за адресою: {address}",
                "success",
            )
            return redirect(url_for("index"))

        return render_template("product_detail.html", product=product)
