from flask import render_template, redirect, flash, url_for, request
from sqlalchemy.orm.util import join
from app.forms import LoginForm, RegistrationForm, CreateTournamentForm, AdminDisciplineForm, AdminTournamentEditForm, SingleDisciplineForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Tournaments, Users, Disciplines, TournamentsDisciplinesMap, TournamentsPlayersMap, Results, Score


from app import app, engine
from sqlalchemy import delete, desc,  asc, func
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
    tournament = session.query(Tournaments).order_by(desc(Tournaments.Season)).first()
    disciplinelist =  session.query(TournamentsDisciplinesMap, Disciplines).join(Disciplines, (TournamentsDisciplinesMap.ID_discipline == Disciplines.ID)).filter(TournamentsDisciplinesMap.ID_tournament == tournament.ID)
    return render_template('disciplines.html', current_user=current_user, disciplinelist=disciplinelist)

@app.route('/disciplines/<discipline>', methods=['GET', 'POST'])
@login_required
def discipline(discipline):
    tournament = session.query(Tournaments).order_by(desc(Tournaments.Season)).first()
    disciplinelist =  session.query(TournamentsDisciplinesMap, Disciplines).join(Disciplines, (TournamentsDisciplinesMap.ID_discipline == Disciplines.ID)).filter(TournamentsDisciplinesMap.ID_tournament == tournament.ID)

    for d in disciplinelist:
        if d[1].Name == discipline:
            print('Discpiline to render found')
            if d[1].type == 'Single':
                form = SingleDisciplineForm()
                if form.validate_on_submit():
                    player = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_users == current_user.ID).first()

                    if session.query(Results).filter(Results.ID_discipline == d[1].ID, Results.ID_tournament == tournament.ID, Results.ID_players == player.ID).count() > 0:
                        
                        #update tournament result of the given user and discipline DB...
                        result = session.query(Results).filter(Results.ID_discipline == d[1].ID, Results.ID_tournament == tournament.ID, Results.ID_players == player.ID)
                        #TODO: date changed does not work yet (update not possible due to not workingfunc.current_timestamp())
                        #.update({'DateChanged': (func.current_timestamp())})

                        #create the score entry and link it to the result entry in the DB...
                        score = session.query(Score).filter(Score.ID_result == result[0].ID).update({'Score': (form.score.data)})
                        session.add(score)
                        session.commit()

                        flash('Score modified!')
                    else:

                        #create tournament result of the given user and discipline DB...
                        result = Results(DateCreated=func.current_timestamp(), DateChanged=func.current_timestamp(), ID_discipline=d[1].ID, ID_tournament=tournament.ID, ID_players=player.ID)
                        session.add(result)
                        session.commit()

                        #create the score entry and link it to the result entry in the DB...
                        print(result.ID)
                        score = Score(ID_result=result.ID, Score=form.score.data)
                        session.add(score)
                        session.commit()

                        flash('Score added!')

                return render_template('discipline_single.html', current_user=current_user, discipline=d, form=form)
            elif d[1].type == 'OneVsOne':
                form = SingleDisciplineForm()
                return render_template('discipline_one_vs_one.html', current_user=current_user, discipline=d, form=form)

    return "Record not found", 400

@app.route('/disciplines/results')
@login_required
def results():
    tournament = session.query(Tournaments).order_by(desc(Tournaments.Season)).first()
    disciplinelist =  session.query(TournamentsDisciplinesMap, Disciplines).join(Disciplines, (TournamentsDisciplinesMap.ID_discipline == Disciplines.ID)).filter(TournamentsDisciplinesMap.ID_tournament == tournament.ID)
    return render_template('results.html', current_user=current_user, disciplinelist=disciplinelist)


@app.route('/disciplines/result/<discipline>', methods=['GET', 'POST'])
@login_required
def result(discipline):
    tournament = session.query(Tournaments).order_by(desc(Tournaments.Season)).first()
    disciplinelist =  session.query(TournamentsDisciplinesMap, Disciplines).join(Disciplines, (TournamentsDisciplinesMap.ID_discipline == Disciplines.ID)).filter(TournamentsDisciplinesMap.ID_tournament == tournament.ID)

    for d in disciplinelist:
        if d[1].Name == discipline:
            print('Discpiline to render found')
            if d[1].type == 'Single':
                #prepare/get table params...
                num_players = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_tournament == tournament.ID).count()
                print('There are %d players', num_players)

                #get table data from DB...
                results = session.query(Results, Score, TournamentsPlayersMap, Users).join(Score, (Score.ID_result == Results.ID)).join(TournamentsPlayersMap, (Results.ID_players == TournamentsPlayersMap.ID)).join(Users, (TournamentsPlayersMap.ID_users == Users.ID)).filter(Results.ID_discipline == d[1].ID).order_by(desc(Score.Score))

#                session.query(Users).join(TournamentsPlayersMap, (Users.ID == TournamentsPlayersMap.ID_users)).filter(r[0].ID_players == TournamentsPlayersMap.ID).count()

                for r in results:
                    print(r)

                return render_template('result_discipline_single.html', current_user=current_user, discipline=d, num_players=num_players, results=results)
            elif d[1].type == 'OneVsOne':
                return render_template('result_discipline_one_vs_one.html', current_user=current_user, discipline=d)

    return "Record not found", 400


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

    for t in tournamentlist:
        print(t)

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
            session.commit()
            flash('discipline deleted!')

    disciplinelist = session.query(Disciplines.Name, Disciplines.type)

    tournamenteditform = AdminTournamentEditForm()
    
    if tournamenteditform.validate_on_submit():
        if tournamenteditform.adddiscipline.data:
            mapping = TournamentsDisciplinesMap(ID_tournament=tournamenteditform.data['tournamentselect'].ID, ID_discipline=tournamenteditform.data['disciplineselect'].ID)
            session.add(mapping)
            session.commit()
            flash('discipline added to tournament!')
        elif tournamenteditform.removediscipline.data:
#            stmt = delete(TournamentsDisciplinesMap).where(TournamentsDisciplinesMap.ID_tournament == tournamenteditform.data['tournamentselect'].ID, TournamentsDisciplinesMap.ID_discipline == tournamenteditform.data['disciplineselect'].ID).execution_options(synchronize_session="fetch")
#            session.execute(stmt)
            session.query(TournamentsDisciplinesMap).filter(TournamentsDisciplinesMap.ID_tournament == tournamenteditform.data['tournamentselect'].ID, TournamentsDisciplinesMap.ID_discipline == tournamenteditform.data['disciplineselect'].ID).delete()
            session.commit()
            flash('discipline removed from tournament!')

        if tournamenteditform.addplayer.data:
            if session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_tournament == tournamenteditform.data['tournamentselect'].ID, TournamentsPlayersMap.ID_users == tournamenteditform.data['playerselect'].ID).count() < 1:
                mapping = TournamentsPlayersMap(ID_tournament=tournamenteditform.data['tournamentselect'].ID, ID_users=tournamenteditform.data['playerselect'].ID, status='active')
                session.add(mapping)
            else:
                session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_tournament == tournamenteditform.data['tournamentselect'].ID, TournamentsPlayersMap.ID_users == tournamenteditform.data['playerselect'].ID).update({'status': ('active')})
            session.commit()
            flash('player added to tournament!')
        elif tournamenteditform.removeplayer.data:
            session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_tournament == tournamenteditform.data['tournamentselect'].ID, TournamentsPlayersMap.ID_users == tournamenteditform.data['playerselect'].ID).update({'status': ('inactive')})
            session.commit()
            flash('player deactivated from tournament!')
        elif tournamenteditform.save.data:
            print('save pressed')
        else:
            print('nothing pressed')

    print(tournamenteditform.errors)

    tournamentselectlist = None
    playerselectlist = None
    if tournamenteditform.tournamentselect.data is not None:
        #quey all desciplines which are linked to the given tournament
        tournamentselectlist = session.query(Disciplines).join(TournamentsDisciplinesMap, (TournamentsDisciplinesMap.ID_discipline == Disciplines.ID))
        playerselectlist = session.query(Users).join(TournamentsPlayersMap, (TournamentsPlayersMap.ID_users == Users.ID)).filter(TournamentsPlayersMap.status == 'active')
        for t in tournamentselectlist:
            print(t)

        for p in playerselectlist:
            print(p)

        print('ttt------------------')

    

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
    return render_template('admin_menu.html', title='Admin', form=form, disciplineform=disciplineform, tournamenteditform=tournamenteditform, current_user=current_user, tournamentlist=tournamentlist, disciplinelist=disciplinelist, tournamentselectlist=tournamentselectlist, playerselectlist=playerselectlist)

@app.route('/news')
def news():
    return render_template('news.html', current_user=current_user)
