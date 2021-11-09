from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email
from flask_ckeditor import CKEditorField, CKEditor
from flask_bootstrap import Bootstrap
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("export MY_PASSWORD")
MAIN_EMAIL = os.environ.get("MAIN_EMAIL")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
ckeditor = CKEditor(app)
Bootstrap(app)


class ConnectForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()], render_kw={"placeholder": "Name"})
    email = StringField("Email", validators=[InputRequired(), Email(message="That's not a valid email address.")],
                        render_kw={"placeholder": "Email Address"})
    message = CKEditorField("Message", validators=[DataRequired()], render_kw={"placeholder": "Message", "rows": "5"})
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def home():
    form = ConnectForm()
    current_year = datetime.datetime.now().year
    if request.method == "POST" and form.validate_on_submit():
        data = request.form
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr="MY_EMAIL",
                                to_addrs="MAIN_EMAIL",
                                msg=f"Subject:Message from your personal site\n\nName: {data['name']}\n"
                                    f"Email: {data['email']}\nMessage: {data['message']}")

        return redirect(url_for('home'))
    return render_template('index.html', form=form, year=current_year)



if __name__ == '__main__':
    app.run(debug=True)