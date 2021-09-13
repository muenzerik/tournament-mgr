from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired
from app.models import Users, Tournaments

from app import app, engine
from sqlalchemy.orm import Session
session = Session(engine)

#User Login Stuff...

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = session.query(Users).filter_by(UserName=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = session.query(Users).filter_by(Email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

#Admin Stuff...

class CreateTournamentForm(FlaskForm):
    name = StringField('Tournament Name', validators=[DataRequired()])
    season = DateField('Season', validators=[InputRequired()], format='%Y')
    create = SubmitField('Create')

    def validate_tournament_creation(self, name):
        names = session.query(Tournaments).filter_by(Name=name.data).first()
        if names is not None:
            raise ValidationError('Please use a different name.')

    #TODO: Validate season not older than now

    #TODO: Validate no entry with same name AND season
