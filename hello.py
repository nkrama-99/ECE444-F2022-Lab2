from crypt import methods
from email.message import EmailMessage
from ensurepip import bootstrap
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email Address?', validators=[Email()])
    submit = SubmitField('Submit')
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ML7Fkdnrd4'
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    
    emailMessage = None
    currEmail = session.get('email')
    
    if not currEmail:
        emailMessage = None
    elif "utoronto" not in currEmail:
        emailMessage = "Please use your UofT email."
    else:
        emailMessage = "Your UofT email is " + currEmail
        
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           emailMessage=emailMessage)

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)