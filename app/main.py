import psycopg2
from flask import Flask
import os


app = Flask(__name__)
conn = psycopg2.connect(
    host="db",
    database="postgres",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
)


def init_db():
    with conn.cursor() as curs, open("init.sql") as file:
        curs.execute(file.read())
    conn.commit()


init_db()


@app.route("/")
def index():
    return f"<p>Hello, World!</p><p>{conn}</p>"


if __name__ == "__main__":
    app.run()
