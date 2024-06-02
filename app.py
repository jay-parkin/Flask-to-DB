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

# CLI commands
# python3 -m flask create
@app.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables Created..")

@app.cli.command("seed")
def seed_tables():
    # Create a product object
    products = [
        {"name": "Smartphone", "price": "$799", "description": "High-performance smartphone with advanced camera features.", "stock": 35},
        {"name": "Laptop", "price": "$1299", "description": "Lightweight laptop with exceptional battery life and powerful processor.", "stock": 20},
        {"name": "Headphones", "price": "$199", "description": "Noise-cancelling headphones with superior sound quality.", "stock": 50},
        {"name": "Smartwatch", "price": "$349", "description": "Stylish smartwatch with health and connectivity features.", "stock": 45},
        {"name": "Tablet", "price": "$499", "description": "Versatile tablet perfect for entertainment and productivity.", "stock": 30},
        {"name": "Camera", "price": "$699", "description": "Digital camera with high resolution and powerful zoom capabilities.", "stock": 25},
        {"name": "Gaming Console", "price": "$399", "description": "Next-gen gaming console with immersive graphics and gameplay.", "stock": 40},
        {"name": "Fitness Tracker", "price": "$129", "description": "Compact fitness tracker with sleep monitoring and GPS.", "stock": 60},
        {"name": "Desktop Computer", "price": "$999", "description": "High-powered desktop perfect for gaming and professional use.", "stock": 15},
        {"name": "Bluetooth Speaker", "price": "$149", "description": "Portable Bluetooth speaker with excellent sound clarity and bass.", "stock": 70},
        {"name": "Wireless Earbuds", "price": "$199", "description": "True wireless earbuds with touch controls and long battery life.", "stock": 55},
        {"name": "External Hard Drive", "price": "$129", "description": "High-capacity external hard drive, perfect for backups.", "stock": 40},
        {"name": "Printer", "price": "$249", "description": "Efficient multi-functional printer for home or office use.", "stock": 30},
        {"name": "Electric Toothbrush", "price": "$79", "description": "Electric toothbrush with multiple brushing modes and timer.", "stock": 90},
        {"name": "Air Purifier", "price": "$299", "description": "High-efficiency air purifier to enhance indoor air quality.", "stock": 35},
        {"name": "Coffee Maker", "price": "$129", "description": "Fast-brewing coffee maker with customizable strength settings.", "stock": 45},
        {"name": "Robot Vacuum Cleaner", "price": "$349", "description": "Smart robot vacuum cleaner with multi-room navigation.", "stock": 38},
        {"name": "Wireless Router", "price": "$99", "description": "High-speed wireless router with extensive coverage and security features.", "stock": 65},
        {"name": "Smart Thermostat", "price": "$199", "description": "Energy-efficient smart thermostat with remote control capabilities.", "stock": 50},
        {"name": "Bluetooth Headset", "price": "$79", "description": "Lightweight Bluetooth headset with clear audio and long battery life.", "stock": 75}
    ]

    count = 0
    for product in products:
        
        product_obj = Product()
        product_obj.name = product["name"]
        product_obj.price = float(product["price"].replace("$", ""))
        product_obj.description = product["description"]
        product_obj.stock = product["stock"]

        # add to session
        db.session.add(product_obj)

        count += 1

    #commit
    db.session.commit()

    print(f"{count} Tables seeded..")

@app.cli.command("drop")
def drop_tables():
    db.drop_all()

    print("Tables Dropped..")




