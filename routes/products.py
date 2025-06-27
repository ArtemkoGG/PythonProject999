from flask import Flask, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Order
from settings import Session
from app import app
from pytz import timezone, UTC


@app.route("/products")
@login_required
def products():
    kyiv_tz = timezone("Europe/Kyiv")

    with Session() as session:
        orders = (
            session.query(Order)
            .filter(Order.user_id == current_user.id)
            .order_by(Order.order_time.desc())
            .all()
        )

        for order in orders:
            order.order_time = order.order_time.replace(
                tzinfo=UTC).astimezone(kyiv_tz)

    return render_template("products.html", orders=orders)
