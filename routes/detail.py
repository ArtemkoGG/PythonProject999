from flask import render_template, abort
from models import Product
from settings import Session
from app import app

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    with Session() as session:
        product = session.get(Product, product_id)
        if not product:
            abort(404)
        return render_template("product_detail.html", product=product)