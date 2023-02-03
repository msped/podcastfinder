import os
from flask import Flask
from dotenv import load_dotenv
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECERT_KEY")
app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=True)