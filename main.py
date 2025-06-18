import random
import os
from functools import wraps
import smtplib
from dotenv import load_dotenv
from flask import Flask,render_template, redirect, url_for, flash, abort
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String,Boolean
from forms import  RegisterForm, LoginForm, SearchForm, AddForm, UpdatePriceForm, AddMenuItemsToDatabaseForm, AddMenuItemsToCafeForm

#LOAD ENV VARIABLES
load_dotenv()

#CONFIGURE FLASK APP
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap5(app)

#CONFIGURE USER LOGIN
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(customer_id):
    return db.session.execute(db.select(Customers).where(Customers.id == customer_id)).scalar()

#CREATE DB
class Base(DeclarativeBase):
    pass
#CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#CONFIGURE TABLE

#ASSOCIATION TABLE TO ESTABLISH MANY TO MANY RELATIONSHIP - CAFES <--> MENU ITEMS
cafe_menu = db.Table("cafe_menu",
                     db.Column("cafe_id", db.Integer, db.ForeignKey("cafe.id")),
                     db.Column("menu_item_id", db.Integer, db.ForeignKey("menu_item.id")))

#ASSOCIATION TABLE TO ESTABLISH MANY TO MANY RELATIONSHIP - CAFES <--> CUSTOMERS
cafe_customer = db.Table("cafe_customer",
                         db.Column("cafe_id", db.Integer, db.ForeignKey("cafe.id")),
                         db.Column("customer_id", db.Integer, db.ForeignKey("customer.id")))



class Cafes(db.Model):
    __tablename__ = "cafe"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url : Mapped[str] = mapped_column(String(500), nullable=False)
    img_url : Mapped[str] = mapped_column(String(500), nullable=False)
    location : Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets : Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_toilet : Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi : Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls : Mapped[bool] = mapped_column(Boolean, nullable=False)
    seats : Mapped[str] = mapped_column(String(250))
    coffee_price : Mapped[str] = mapped_column(String(250))
    menu_items = relationship("MenuItems", secondary=cafe_menu, back_populates="cafes")
    customers = relationship("Customers",secondary=cafe_customer, back_populates="cafes")

class MenuItems(db.Model):
    __tablename__ = "menu_item"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    img_url : Mapped[str] = mapped_column(String, nullable=False)
    price : Mapped[int] = mapped_column(Integer, nullable=False)
    cafes = relationship("Cafes", secondary=cafe_menu, back_populates="menu_items")
    cart = relationship("Carts",back_populates="original_item" )

class Customers(UserMixin ,db.Model):
    __tablename__ = "customer"
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password : Mapped[str] = mapped_column(String, nullable=False)
    address : Mapped[str] = mapped_column(String, nullable=False)
    cafes = relationship("Cafes", secondary=cafe_customer, back_populates="customers")
    cart_items = relationship("Carts", back_populates="customer")

class Carts(db.Model):
    __tablename__ = "cart"
    item_id : Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id : Mapped[int] = mapped_column(Integer, db.ForeignKey("customer.id"))
    customer = relationship("Customers", back_populates="cart_items")
    original_item_id : Mapped[int] = mapped_column(Integer, db.ForeignKey("menu_item.id"))
    original_item = relationship("MenuItems", back_populates="cart")


with app.app_context():
    db.create_all()

#LOGIN REQUIRED DECORATED FUNCTION
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You are not logged in yet! please login")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

#ADMIN ONLY - DECORATED FUNCTION
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

#CUSTOMER REGISTERATION
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user_already_exist = db.session.execute(db.select(Customers).where(Customers.email == email)).scalar()
        if user_already_exist:
            flash("looks like you have already registered! try login instead")
            return redirect(url_for("login"))

        hashed_and_salted_password = generate_password_hash(password=form.password.data,
                                                            method="pbkdf2:sha256",
                                                            salt_length=8)
        name = form.name.data
        address = form.address.data
        new_customer = Customers(name = name,
                                 email = email,
                                 password = hashed_and_salted_password,
                                 address = address
                                 )
        db.session.add(new_customer)
        db.session.commit()
        login_user(new_customer)
        return redirect(url_for("show_all_cafes"))

    return render_template("register.html", form=form, current_user = current_user)


#CUSTOMER LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user_already_exist = db.session.execute(db.select(Customers).where(Customers.email == email)).scalar()
        if not user_already_exist:
            flash("Email does not exist! Please try again")
            return redirect(url_for("login"))

        if not check_password_hash(user_already_exist.password, form.password.data):
            flash("Incorrect Password! Please try again")
            return redirect(url_for("login"))

        else:
            login_user(user_already_exist)
            return redirect(url_for("show_all_cafes"))

    return render_template("login.html", form = form, current_user = current_user)

#CUSTORMER LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("show_all_cafes"))

#RENDERS HOMEPAGE AND DISPLAY ALL THE CAFE
@app.route("/")
def show_all_cafes():
    result = db.session.execute(db.select(Cafes))
    all_cafes = result.scalars().all()
    return render_template("index.html", cafes = all_cafes, current_user = current_user)

#RENDERS CAFE DETAILS
@app.route("/cafe-details/<int:cafe_id>")
def show_cafe(cafe_id):
    requested_cafe = db.session.execute(db.select(Cafes).where(Cafes.id == cafe_id)).scalar()
    return render_template("show_cafe.html", cafe = requested_cafe, current_user = current_user)

#RENDERS FORM TO SEARCH A CAFE BY LOCATION
@app.route("/search", methods=["GET", "POST"])
def search_by_location():
    form = SearchForm()
    all_cafes=[]
    if form.validate_on_submit():
        requested_location = form.location.data.title()
        result = db.session.execute(db.select(Cafes).where(Cafes.location == requested_location))
        all_cafes = result.scalars().all()
        if not all_cafes:
            flash("We dont have a cafe information at the searched location.")
    return render_template("search.html", form=form, cafes=all_cafes, current_user = current_user)

#RENDERS RANDOM CAFE DETAILS
@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafes))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return render_template("show_cafe.html", cafe = random_cafe, current_user = current_user)

#RENDERS FORM TO ADD A NEW CAFE TO THE WEBSITE
@app.route("/add_cafe", methods=["GET", "POST"])
@login_required
def add_cafe():
    form = AddForm()
    if form.validate_on_submit():
        already_exist = db.session.execute(db.select(Cafes).where(Cafes.name == form.name.data)).scalar()
        if already_exist:
            flash("Cafe already exist on the website.")
            return redirect(url_for("add_cafe"))
        else:
            new_cafe = Cafes(
                name = form.name.data,
                map_url = form.map_url.data,
                img_url = form.img_url.data,
                location = form.location.data,
                has_sockets = form.has_sockets.data,
                has_toilet = form.has_toilet.data,
                has_wifi = form.has_wifi.data,
                can_take_calls = form.can_take_calls.data,
                seats = form.seats.data,
                coffee_price = form.coffee_price.data
            )
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for("show_all_cafes"))
    return render_template("add.html", form = form, current_user = current_user)

#RENDERS FORM TO UPDATE A COFFEE PRICE AT A CAFE
@app.route("/edit_price/<int:cafe_id>", methods=["GET", "POST"])
@login_required
def update_price(cafe_id):
    form = UpdatePriceForm()
    if form.validate_on_submit():
        requested_cafe = db.session.execute(db.select(Cafes).where(Cafes.id == cafe_id)).scalar()
        requested_cafe.coffee_price = form.updated_price.data
        db.session.commit()
        return redirect(url_for("show_cafe", cafe_id = requested_cafe.id))

    return render_template("update_price.html", form = form, current_user = current_user)

@app.route("/add_menu_item_to_database", methods=["GET", "POST"])
@admin_only
def add_menu_items_to_database():
    form = AddMenuItemsToDatabaseForm()
    if form.validate_on_submit():
        item_already_exist = db.session.execute(db.select(MenuItems).where(MenuItems.name == form.name.data)).scalar()
        if item_already_exist:
            flash("This Menu Item already exist in the Database!")
        new_item = MenuItems(
            name = form.name.data,
            img_url = form.img_url.data,
            price = int(form.price.data)
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("show_all_cafes"))
    return render_template("add_menu_item_to_database.html", form = form, current_user = current_user)

#MANAGE MENU ITEMS AT A CAFE
@app.route("/manage_menu_at_cafe<int:cafe_id>", methods=["GET", "POST"])
@admin_only
def manage_menu_at_cafe(cafe_id):
    current_cafe = db.session.execute(db.select(Cafes).where(Cafes.id == cafe_id)).scalar()
    form = AddMenuItemsToCafeForm()
    form.cafe_name.data = current_cafe.name

    menu_items = current_cafe.menu_items

    if form.validate_on_submit():
        item = db.session.execute(db.select(MenuItems).where(MenuItems.name == form.item_name.data.title())).scalar()
        if form.item_name.data in[item.name for item in menu_items]:
            flash("This Menu item is already added to this Cafe!")
        new_menu_at_cafe = cafe_menu.insert().values(cafe_id = cafe_id, menu_item_id = item.id)
        db.session.execute(new_menu_at_cafe)
        db.session.commit()
        return redirect(url_for("manage_menu_at_cafe", cafe_id = current_cafe.id))
    return render_template("manage_menu_at_cafe.html", form = form, menu_items = menu_items, cafe=current_cafe, current_user=current_user)

#REMOVE MENU ITEM FROM CAFE
@app.route("/remove_menuitem_at_cafe/<int:item_id>/<int:cafe_id>")
@admin_only
def remove_menu_item_at_cafe(item_id, cafe_id):
    item_to_delete = cafe_menu.delete().where(
        cafe_menu.c.cafe_id == cafe_id,
        cafe_menu.c.menu_item_id == item_id
    )
    db.session.execute(item_to_delete)
    db.session.commit()
    return redirect(url_for("manage_menu_at_cafe", cafe_id = cafe_id))



#RENDERS THE MENU ITEM AT THE SELECTED CAFE
@app.route("/show_menu/<int:cafe_id>")
def show_menu(cafe_id):
    current_cafe = db.session.execute(db.select(Cafes).where(Cafes.id == cafe_id)).scalar()
    menu_items = current_cafe.menu_items
    return render_template("menu.html", menu_items = menu_items, cafe= current_cafe, current_user = current_user )

#ADD ITEM TO  CART FOR A CUSTOMER
@app.route("/add_to_cart/<int:item_id>/<int:cafe_id>")
@login_required
def add_to_cart(item_id, cafe_id):
    add_item = Carts(
        customer_id = current_user.id,
        original_item_id = item_id
    )
    db.session.add(add_item)
    db.session.commit()
    return redirect(url_for("show_menu", cafe_id = cafe_id))

@app.route("/checkout")
@login_required
def checkout():
    cart_items =[cart.original_item for cart in current_user.cart_items]
    total_bill = sum(item.price for item in cart_items)
    return render_template("check_out.html", cart_items = cart_items, current_user = current_user, total_bill = total_bill)

@app.route("/send_order_confirmation")
@login_required
def send_order_confirmation():
    cart_items = [cart.original_item for cart in current_user.cart_items]
    total_bill = sum(item.price for item in cart_items)
    order_details = ""
    for item in cart_items:
        order_details += f"\n{item.name} : £ {item.price}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user = os.environ.get("EMAIL"),
                         password=os.environ.get("GMAIL_APP_PASSWORD"))
        connection.sendmail(from_addr=os.environ.get("EMAIL"),
                            to_addrs=current_user.email,
                            msg=f"Subject:Order Confirmation!\n\nHello {current_user.name} "
                                f"\nyour order has been confirmed & will be delivered soon."
                                f"\nplease find order detail below:-"
                                f"{order_details}"
                                f"\nTotal_bill = £ {total_bill}"
                                f"\nBilling Address : {current_user.address}".encode("utf-8"))
        connection.close()
    remove_cart = db.session.execute(db.select(Carts).where(Carts.customer_id == current_user.id)).scalars().all()
    for item in remove_cart:
        db.session.delete(item)
    db.session.commit()
    return render_template("confirm_order.html")



if __name__ == "__main__":
    app.run(debug=True)