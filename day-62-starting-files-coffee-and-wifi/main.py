from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, url
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps (URL)', validators=[DataRequired(), url()])
    open_time = StringField('Opening time e.g.8AM', validators=[DataRequired()])
    close_time = StringField('Closing time e.g.9.30PM', validators=[DataRequired()])
    coffee_rating = SelectField(u'Coffee Ratings', choices=['☕', '☕ ☕', '☕ ☕ ☕', '☕ ☕ ☕ ☕', '☕ ☕ ☕ ☕ ☕'])
    wifi_rating = SelectField(u'Wifi Strength Ratings', choices=['✘', '💪', '💪 💪', '💪 💪 💪', '💪 💪 💪 💪', '💪 💪 💪 💪 💪'])
    power_socket = SelectField(u'Power Socket Availability', choices=['✘', '🔌', '🔌 🔌', '🔌 🔌 🔌', '🔌 🔌 🔌', '🔌 🔌 🔌 🔌', '🔌 🔌 🔌 🔌 🔌'])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power  outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


# Exercise:
# Make the form write a new row into cafe-data.csv
# with   if form.validate_on_submit()
@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        c_name = form.cafe.data
        c_location = form.location.data
        c_open = form.open_time.data
        if "AM" not in c_open:
            c_open += "AM"
        c_close = form.close_time.data
        if "PM" not in c_close:
            c_close += "PM"
        c_rating = form.coffee_rating.data
        w_rating = form.wifi_rating.data
        s_rating = form.power_socket.data
        with open("cafe-data.csv", mode="a") as csv_file:
            csv_file.write(f"\n{c_name},{c_location}, {c_open}, {c_close}, {c_rating}, {w_rating},{s_rating}")

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)


# Completed !!!

