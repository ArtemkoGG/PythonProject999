from flask import render_template
from app import app
from models import Product
from settings import Session

@app.route('/asortiment')
def asortiment():
    with Session() as session:
        products = session.query(Product).all()
    return render_template('asortiment.html', products=products, name_restaurant="Смачно Онлайн")