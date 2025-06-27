import os
import uuid
from flask import flash, render_template, request
from app import app, admin_required
from models import Asortiment
from settings import Session, config


@app.route("/admin/add_position", methods=["GET", "POST"])
@admin_required
def add_position():
    if request.method == "POST":

        name = request.form["name"]
        file = request.files.get("img")
        description = request.form["description"]
        price = request.form["price"]

        if not file or not file.filename:
            return "Файл не вибрано або завантаження не вдалося"

        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        output_path = os.path.join("static/menu", unique_filename)

        with open(output_path, "wb") as f:
            f.write(file.read())

        with Session() as cursor:
            new_position = Asortiment(
                name=name,
                description=description,
                price=price,
                file_name=unique_filename,
            )
            cursor.add(new_position)
            cursor.commit()

        flash("Позицію додано успішно!")

    return render_template(
        "admin/add_position.html", name_restaurant=config.NAME_RESTAURNAT
    )
