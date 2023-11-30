import os

import psycopg2
from flask import Flask, render_template, request, redirect

from db import SelectDescriptorsEnum, fake
from db import init_db, add_person, delete_person
from db import iter_datalist, get_table_items

app = Flask(__name__)
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database="postgres",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
)

init_db(conn)


@app.route("/")
def index():
    return render_template('index.html', conn=conn)


@app.route("/add/", methods=("GET", "POST"))
def add():
    form = request.form
    if request.method == "POST" and add_person(conn, form.to_dict()):
        form = dict()
    context = {desc.name: [form.get(desc.value.key, desc.value.fake_factory()),
                           *iter_datalist(conn, desc)] for desc in SelectDescriptorsEnum}
    context |= {
        "building": form.get('building', fake.building_number()),
        "phone": form.get('phone', fake.phone_number())
    }
    return render_template('add.html', **context)


@app.route("/table")
def table():
    page = int(request.args.get('page', 0))
    search = request.args.get('search', '')
    items = get_table_items(conn, page, search)
    return render_template('table.html',
                           page=page, search=search, items=items)


@app.route("/remove", methods=("POST",))
def remove():
    if (person_id := request.form.get('id')) is None:
        return "id not specified", 400
    if not delete_person(conn, int(person_id)):
        return "wrong id", 400
    if n := request.form.get('next'):
        return redirect(n)
    return "success", 200


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", False))
