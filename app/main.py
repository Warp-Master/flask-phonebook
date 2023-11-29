import os

import psycopg2
from faker import Faker
from flask import Flask, render_template, request, redirect, url_for

from db import init_db, add_person

fake = Faker()


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
    if request.method == "POST" and add_person(conn, request.form.to_dict()):
        return redirect(url_for('add'))
    return render_template('add.html',
                           firstnames=[request.form.get('firstname', fake.first_name())],
                           lastnames=[request.form.get('lastname', fake.last_name())],
                           surnames=[request.form.get('surname', fake.passport_owner()[1])],
                           cities=[request.form.get('city', fake.city())],
                           streets=[request.form.get('street', fake.street_name())],
                           building=request.form.get('building', fake.building_number()),
                           phone=request.form.get('phone', fake.phone_number()))


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", False))
