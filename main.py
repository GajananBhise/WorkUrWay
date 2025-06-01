import random
import os
from dotenv import load_dotenv
from flask import Flask,render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String,Boolean
from forms import SearchForm, AddForm, UpdatePriceForm

#LOAD ENV VARIABLES
load_dotenv()

#CONFIGURE FLASK APP
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap5(app)

#CREATE DB
class Base(DeclarativeBase):
    pass
#CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#CONFIGURE TABLE
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

with app.app_context():
    db.create_all()

#RENDERS HOMEPAGE AND DISPLAY ALL THE CAFE
@app.route("/")
def show_all_cafes():
    result = db.session.execute(db.select(Cafes))
    all_cafes = result.scalars().all()
    return render_template("index.html", cafes = all_cafes)

#RENDERS CAFE DETAILS
@app.route("/cafe-details/<int:cafe_id>")
def show_cafe(cafe_id):
    requested_cafe = db.session.execute(db.select(Cafes).where(Cafes.id == cafe_id)).scalar()
    return render_template("show_cafe.html", cafe = requested_cafe)

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
    return render_template("search.html", form=form, cafes=all_cafes)

#RENDERS RANDOM CAFE DETAILS
@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafes))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return render_template("show_cafe.html", cafe = random_cafe)

#RENDERS FORM TO ADD A NEW CAFE TO THE WEBSITE
@app.route("/add_cafe", methods=["GET", "POST"])
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
    return render_template("add.html", form = form)

#RENDERS FORM TO UPDATE A COFFEE PRICE AT A CAFE
@app.route("/edit_price/<int:cafe_id>", methods=["GET", "POST"])
def update_price(cafe_id):
    form = UpdatePriceForm()
    if form.validate_on_submit():
        requested_cafe = db.session.execute(db.select(Cafes).where(Cafes.id == cafe_id)).scalar()
        requested_cafe.coffee_price = form.updated_price.data
        db.session.commit()
        return redirect(url_for("show_cafe", cafe_id = requested_cafe.id))

    return render_template("update_price.html", form = form)

if __name__ == "__main__":
    app.run(debug=False)
