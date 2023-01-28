from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



#Create flask Instance
app = Flask(__name__)


#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#secret key
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


db = SQLAlchemy(app)



#model
class Users(db.Model):
    name = db.Column(db.VARCHAR(60), primary_key=True)
    message = db.Column(db.TEXT)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name



#Form class
class UserForm(FlaskForm):
    name = StringField ('Name', validators=[DataRequired()], render_kw={"placeholder":"Your Name...."})
    message = TextAreaField ('Message', render_kw={"rows": 5, "cols": 50, "placeholder":"Your Message...."}, validators=[DataRequired()])
    submit = SubmitField ('Submit')


@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/about')
def abt():
    return render_template('about.html')

@app.route('/edu')
def edu():
    return render_template('edu.html')

@app.route('/exp')
def exp():
    return render_template('exp.html')

@app.route('/wrk')
def wrk():
    return render_template('wrk.html')



@app.route('/contact', methods=['GET', 'POST'])
def cont():
    name = None
    form = UserForm()
    #validating form
    if form.validate_on_submit():
        user=Users(name = form.name.data, message = form.message.data)
        db.session.add(user)
        db.session.commit()
        name= form.name.data
        form.name.data=''
        form.message.data=''
        flash('Message submitted successfully!')
    our_users=Users.query.order_by(Users.date_added)
    return render_template('contact.html', form = form, our_users=our_users, name=name)

@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    name = None
    form = UserForm()
    #validating form
    if form.validate_on_submit():
        user=Users(name = form.name.data, message = form.message.data)
        db.session.add(user)
        db.session.commit()
        name= form.name.data
        form.name.data=''
        form.message.data=''
        flash('Message submitted successfully!')
    our_users=Users.query.order_by(Users.date_added)
    return render_template('dashboard.html', form = form, our_users=our_users, name=name)
    
