from flask import render_template, redirect, flash, url_for, request
from app.forms import LoginForm, RegistrationForm, CreateTournamentForm, AdminDisciplineForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Tournaments, Users, Disciplines


from app import app, engine
from sqlalchemy import delete
from sqlalchemy.orm import Session
session = Session(engine)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(Users).filter_by(UserName=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form, current_user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(UserName=form.username.data, Email=form.email.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, current_user=current_user)

@app.route('/disciplines')
@login_required
def disciplines():
    return render_template('disciplines.html', current_user=current_user)

@app.route('/time_schedule')
@login_required
def time_schedule():
    return render_template('time_schedule.html', current_user=current_user)

@app.route('/image_gallery')
@login_required
def image_gallery():
    return render_template('image_gallery.html', current_user=current_user)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_menu():
    form = CreateTournamentForm()
    if form.validate_on_submit():
        #TODO: check whether it already exists

        #create tournament in DB
        tournament = Tournaments(Name=form.name.data, Season=form.season.data)
        session.add(tournament)
        session.commit()
        flash('Tornament Created!')

    tournamentlist = session.query(Tournaments.Name, Tournaments.Season)

    disciplineform = AdminDisciplineForm()
    if disciplineform.validate_on_submit():
        #TODO: check whether it already exists

        discipline = Disciplines(Name=disciplineform.name.data, type=dict(disciplineform.type.choices).get(disciplineform.type.data))

        if disciplineform.action.data == 'create':
            session.add(discipline)
            session.commit()
            flash('discipline created!')
        elif disciplineform.action.data == 'modify':
            flash('discipline modified!')
        elif disciplineform.action.data == 'delete':
            stmt = delete(Disciplines).where(Disciplines.Name == disciplineform.name.data and Disciplines.type == dict(disciplineform.type.choices).get(disciplineform.type.data) ).execution_options(synchronize_session="fetch")
            session.execute(stmt)

#            session.delete(discipline)
            session.commit()
            flash('discipline deleted!')


    disciplinelist = session.query(Disciplines.Name, Disciplines.type)

    for t in tournamentlist:
        print(t)

    if request.method == "POST":
        if request.form.get('create'):
            


            print('create')
            pass
        elif request.form.get('manage'):
            # do something else
            pass
    elif request.method == 'GET':
        # do something
        pass
    return render_template('admin_menu.html', title='Admin', form=form, disciplineform=disciplineform, current_user=current_user, tournamentlist=tournamentlist, disciplinelist=disciplinelist)

@app.route('/news')
def news():
    return render_template('news.html', current_user=current_user)
