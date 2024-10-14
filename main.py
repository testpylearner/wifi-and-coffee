from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import smtplib



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = StringField('Power (1 for Yes, 0 for No)', validators=[DataRequired()])
    has_toilet = StringField('Toilet (1 for Yes, 0 for No)', validators=[DataRequired()])
    has_wifi = StringField('Wifi (1 for Yes, 0 for No)', validators=[DataRequired()])
    can_take_calls = StringField('Does Take Calls (1 for Yes, 0 for No)', validators=[DataRequired()])
    seats = StringField('# of Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

#CONFIGURE TABLE
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    has_sockets: Mapped[int] = mapped_column(Integer, nullable=False)
    has_toilet: Mapped[int] = mapped_column(Integer, nullable=False)
    has_wifi: Mapped[int] = mapped_column(Integer, nullable=False)
    can_take_calls: Mapped[int] = mapped_column(Integer, nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.id))
    cafes = result.scalars().all()

    return render_template("index.html", cafes=cafes, len=range(len(cafes)), add_in_cafe=True)

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_post = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home') + '#cafes')
    return render_template("add.html", form=form)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    my_email = "your email"
    password = "password"
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('phone')
        message = request.form.get('message')

        # Sending email
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="to address",
                msg=f"Subject: Contact from User\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Subject: {subject}\n"
                    f"Message: {message}"
            )
        return render_template("index.html")
    return render_template("index.html")

@app.route("/cafe/<int:cafe_id>")
def show_cafe_info(cafe_id):
    result = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id))
    post = db.get_or_404(Cafe, cafe_id)
    all_cafes = result.scalars().all()
    if post:
        requested_cafe = all_cafes[0]
        return render_template("cafe.html", cafe=requested_cafe, add_in_cafe=False)


if __name__ == '__main__':
    app.run(debug=True)
