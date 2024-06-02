from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# connect to database                   dms        db_driver  db_user db_pass   URL     PORT db_name   
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://feb_dev:123456@localhost:5432/feb_db"

db = SQLAlchemy(app)

# Model - table
class Product(db.Model):
    # define the tablename
    __tablename__ = "products"

    # define the primary key
    id = db.Column(db.Integer, primary_key=True)
    # more attributes (columns)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

#  CLI commands
@app.cli.command("create")
def create_db():
    db.create_all()