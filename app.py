from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# connect to database                   dms        db_driver  db_user db_pass   URL     PORT db_name   
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://feb_dev:123456@localhost:5432/feb_db"

db = SQLAlchemy(app)
ma = Marshmallow(app)

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

# Schema
# Help to convert sqlalchemy to python
class ProductSchema(ma.Schema):
    class Meta:
        # fields
        fields = ( "id", "name", "description", "price", "stock" )


# to handle multiple products
products_schema = ProductSchema(many=True)

# to handle single product
product_schema = ProductSchema()


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

    db.session.add_all(products_list)
    #commit
    db.session.commit()

    print(f"{count} Tables seeded..")

@app.cli.command("drop")
def drop_tables():
    db.drop_all()

    print("Tables Dropped..")


#  /products, GET => getting all products
#  /products/id, GET => get a signle product whose id is equal to the one in the url
#  /products, POST => create a new product
#  /products/id, PUT/PATCH => edit/update the product whose id is equal to the one in the url
#  /products/id, DELETE => delete the products whose id is equal to the one in the url


@app.route("/products")
def get_products():
    #  SELECT * FROM Products
    # stmt = statement
    stmt = db.select(Product) # Result # [[]]
    products_list = db.session.scalars(stmt) # ScalarResult # []
    data = products_schema.dump(products_list)

    return data

#  using a dynamic route
@app.route("/products/<int:product_id>")
def get_product(product_id):

    #  SELECT * FROM products WHERE id=int:id
    stmt = db.select(Product).filter_by(id = product_id) # Result # [[]]
    product = db.session.scalar(stmt) # ScalarResult # []

    #  return whether the product exists
    if product:
        data = product_schema.dump(product)

        return data
    else:
        return {"error": f"Product with id {product_id} doesn't exist.."}, 404

    

@app.route("/products", methods=["POST"])
def create_product():
    product_fields = request.get_json()

    new_product = Product(
        name = product_fields.get("name"),
        description = product_fields.get("description"),
        price = product_fields.get("price"),
        stock = product_fields.get("stock")
    )

    db.session.add(new_product)
    db.session.commit()

    # print(f"{new_product.get("name")} has been added..")

    return product_schema.dump(new_product), 201

@app.route("/products/<int:product_id>", methods=["PUT", "PATCH"])
def update_product(product_id):

    #  find the product from the database with the id = product_id
    stmt = db.select(Product).filter_by(id = product_id) # Result # [[]]
    product = db.session.scalar(stmt) # ScalarResult # []

    #  retrieve the data from the body of the request
    body_data = request.get_json()
    
    #  update the atributes
    if product:
        product.name = body_data.get("name") or product.name
        product.description = body_data.get("description") or product.description
        product.price = body_data.get("price") or product.price
        product.stock = body_data.get("stock") or product.stock

        #  commit
        db.session.commit()

        #  return something
        return product_schema.dump(product)

    else:
        return {"error": f"Product with id {product_id} doesn't exist"}, 404


@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    stmt = db.select(Product).where(Product.id == product_id)
    product = db.session.scalar(stmt)

    if product:
        db.session.delete(product)

        db.session.commit()

        return {"message": f"Product with id {product_id} has been deleted"}

    else:

        return {"error": f"Product with id {product_id} doesn't exist"}, 404
