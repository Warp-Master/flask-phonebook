import psycopg2 
from flask import Flask
import os


print(os.getenv("POSTGRES_PASSWORD"))

app = Flask(__name__)
conn = psycopg2.connect(
    host="db",
    database="postgres",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
)


@app.route("/")
def index():
    return f"<p>Hello, World!</p><p>{conn}</p>"


if __name__ == "__main__":
    app.run()
