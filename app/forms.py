from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, Required
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Users, Tournaments, Disciplines, TournamentsDisciplinesMap, TournamentsPlayersMap

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

class AdminDisciplineForm(FlaskForm):
    name = StringField('Discipline Name', validators=[DataRequired()])
    type = SelectField(u'Type', choices=[('single', 'Single'), ('onevsone', 'OneVsOne')], validators=[DataRequired()])
    action = SelectField(u'Action', choices=[('create', 'Create'), ('modify', 'Modify'), ('delete', 'Delete')], validators=[DataRequired()])
    submit = SubmitField('Do Action')

    #TODO: Validate unique

class AdminTournamentEditForm(FlaskForm):
    
    def tournament_choices():      
        return session.query(Tournaments).order_by(Tournaments.Name, Tournaments.Season).all()

    tournamentselect = QuerySelectField(u'Select Tournament...',      
                               validators=[DataRequired()],
                               query_factory=tournament_choices,
                               get_label='Name',
                               allow_blank=True)

    def discipline_choices():      
        return session.query(Disciplines).order_by(Disciplines.Name, Disciplines.type).all()

    disciplineselect = QuerySelectField(u'Select Discipline...',      
                               validators=[DataRequired()],
                               query_factory=discipline_choices,
                               get_label='Name',
                               allow_blank=True)
    adddiscipline = SubmitField('Add')
    removediscipline = SubmitField('Remove')

    def player_choices():      
        return session.query(Users).order_by(Users.UserName).all()

    playerselect = QuerySelectField(u'Select Player...',      
                               validators=[DataRequired()],
                               query_factory=player_choices,
                               get_label='UserName',
                               allow_blank=True)
    addplayer = SubmitField('Add')
    removeplayer = SubmitField('Deactivate')

    save = SubmitField('Save')

    #TODO: Validate unique
