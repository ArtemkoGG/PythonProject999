from flask import render_template
from app import app
from models import Asortiment
from settings import Session


@app.route("/asortiment")
def asortiment():
    with Session() as session:
        asortiment_list = session.query(Asortiment).all()
    return render_template(
        "asortiment.html",
        asortiment_list=asortiment_list,
        name_restaurant="Смачно Онлайн",
    )
