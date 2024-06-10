from datetime import timedelta

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

# connect to database                   dms        db_driver  db_user db_pass   URL     PORT db_name   
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://feb_dev:123456@localhost:5432/feb_db"

# needs to move to a environment variable
app.config["JWT_SECRET_KEY"] = "secret" # for test purposes

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


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

class User(db.Model):
    # define the table name
    __tablename__ = "users"

    #define the primary key
    id = db.Column(db.Integer, primary_key=True)

    # more attributes (columns)
    name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

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

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin")

# to handle multiple products
users_schema = UserSchema(many=True, exclude=["password"])

# to handle single product
user_schema = UserSchema(exclude=["password"])

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

    product_count = 0
    for product in products:
        
        product_obj = Product()
        product_obj.name = product["name"]
        product_obj.price = float(product["price"].replace("$", ""))
        product_obj.description = product["description"]
        product_obj.stock = product["stock"]

        # add to session
        db.session.add(product_obj)

        product_count += 1

    # user db
    users = [
        {
            "name": "User 1",
            "email": "user1@email.com",
            "password": bcrypt.generate_password_hash("123456").decode('utf8')
        },
        {
            "name": "Admin User",
            "email": "admin@email.com",
            "password": bcrypt.generate_password_hash("123456").decode('utf8'),
            "is_admin": True
        },
        {
            "name": "User 2",
            "email": "user2@email.com",
            "password": bcrypt.generate_password_hash("123456").decode('utf8')
        },
        {
            "name": "User 3",
            "email": "user3@email.com",
            "password": bcrypt.generate_password_hash("123456").decode('utf8')
        },
        {
            "name": "User 4",
            "email": "user4@email.com",
            "password": bcrypt.generate_password_hash("123456").decode('utf8')
        }
    ]

    user_count = 0
    for user in users:
        
        user_obj = User()
        user_obj.name = user["name"]
        user_obj.email = user["email"]
        user_obj.password = user["password"]
        user_obj.is_admin = user.get("is_admin", False)

        # add to session
        db.session.add(user_obj)

        user_count += 1

    #commit
    db.session.commit()

    print(f"{product_count} Items in the Products Table seeded..")
    print(f"{user_count} Items in the Users Table seeded..")

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
@jwt_required()
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
@jwt_required()
def delete_product(product_id):

    # find whether user login is an admin or not
    is_admin = authoriseAsAdmin()
    if not is_admin:
        return {"error", "Not authorised to delete a product"}, 403

    stmt = db.select(Product).where(Product.id == product_id)
    product = db.session.scalar(stmt)

    if product:
        db.session.delete(product)

        db.session.commit()

        return {"message": f"Product with id {product_id} has been deleted"}

    else:

        return {"error": f"Product with id {product_id} doesn't exist"}, 404

@app.route("/auth/register", methods=["POST"])
def register_user():
    try:
        # body of the request - data of the user
        body_data = request.get_json()

        # extracting password from the body of the request
        password = body_data.get("password")

        # hashing the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf8') # always needs decode('utf8')

        # create a user using the User model
        user = User(
            name = body_data.get("name"),
            email = body_data.get("email"),
            password = hashed_password
        )

        # add to the db session
        db.session.add(user)

        # commit
        db.session.commit()

        # return something back to the user
        return user_schema.dump(user), 201
    
    except IntegrityError:
        return {"error": "Email address already exists!"}, 409

@app.route("/auth/login", methods=["POST"])
def login_user():
    # get the body data
    body_data = request.get_json()

    # find the user with the email
    # SELECT * FROM user WHERE email='user1@email.com';
    stmt = db.select(User).filter_by(email = body_data.get("email"))
    user = db.session.scalar(stmt)

    # if the user exists and password matches
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")): # hash the given password and check hashed password in db
        # create jwt token
        token = create_access_token(identity = str(user.id), expires_delta = timedelta(days = 1))

        # return the token
        return {"token": token, "email": user.email, "is_admin": user.is_admin}

    # else
    else:
        # return an error message
        return {"error": "Invalid email or password!"}, 401
    
def authoriseAsAdmin():
    # get the id of the user from jwt token
    user_id = get_jwt_identity()

    # find the user in the db with that id
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    
    # check whether the user is an admin or not
    return user.is_admin