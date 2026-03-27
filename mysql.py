import os
import pymysql
from flask import Flask

app = Flask(__name__)

connection = pymysql.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)

@app.route('/')
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM instruments")
    return str(cursor.fetchall())