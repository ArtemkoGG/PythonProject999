import os
import uuid
from flask import flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from app import app, admin_required
from models import Asortiment
from settings import Session, config


@app.route("/admin/add_position", methods=["GET", "POST"])
@admin_required
def add_position_view():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        file = request.files.get("img")

        safe_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{safe_filename}"

        upload_folder = "static/menu"
        output_path = os.path.join(upload_folder, unique_filename)
        file.save(output_path)

        output_path = os.path.join(upload_folder, unique_filename)
        file.save(output_path)

        with Session() as session:
            new_position = Asortiment(
                name=name,
                description=description,
                price=price,
                file_name=os.path.join("static/menu", unique_filename),
            )
            session.add(new_position)
            session.commit()

        flash("Позицію додано успішно!", "success")
        return redirect(url_for("add_position_view"))

    return render_template(
        "admin/add_position.html", name_restaurant=config.NAME_RESTAURNAT
    )
