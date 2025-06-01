from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL

#SEARCH BY LOCATION - FORM
class SearchForm(FlaskForm):
    location = StringField(label="Location", validators=[DataRequired()])
    submit = SubmitField(label="Search")

#ADD NEW CAFE TO THE WEBSITE - FORM
class AddForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    map_url = StringField(label="Map URL", validators=[DataRequired(), URL()])
    img_url = StringField(label="Image URL", validators=[DataRequired(),URL()])
    location = StringField(label="Location", validators=[DataRequired()])
    has_sockets = BooleanField(label="has Sockets")
    has_toilet = BooleanField(label="has Washroom")
    has_wifi = BooleanField(label="has WiFi")
    can_take_calls = BooleanField(label="can take Calls")
    seats = StringField(label="Seats")
    coffee_price = StringField(label="Coffee Price")
    submit = SubmitField(label="Add Cafe")

#UPDATE COFFEE PRICE - FORM
class UpdatePriceForm(FlaskForm):
    updated_price = StringField(label="New Price", validators=[DataRequired()])
    submit = SubmitField(label="Update")


