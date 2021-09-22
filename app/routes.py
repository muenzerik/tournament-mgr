from flask import render_template, redirect, flash, url_for, request
from sqlalchemy.orm.util import join
from app.forms import LoginForm, RegistrationForm, CreateTournamentForm, AdminDisciplineForm, AdminTournamentEditForm, SingleDisciplineForm, OneVsOneDisciplineForm, OneVsOneEntryForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Tournaments, Users, Disciplines, TournamentsDisciplinesMap, TournamentsPlayersMap, Results, Score, MatchResult


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
    if tournament is not None:
        disciplinelist =  session.query(TournamentsDisciplinesMap, Disciplines).join(Disciplines, (TournamentsDisciplinesMap.ID_discipline == Disciplines.ID)).filter(TournamentsDisciplinesMap.ID_tournament == tournament.ID)
        current_player = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_tournament == tournament.ID, TournamentsPlayersMap.ID_users == current_user.ID).first()
    else:
        disciplinelist = None
        current_player = None
    return render_template('disciplines.html', current_user=current_user, disciplinelist=disciplinelist, current_player=current_player)

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
                    #get player info of current user
                    player = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_users == current_user.ID).first()

                    if session.query(Results).filter(Results.ID_discipline == d[1].ID, Results.ID_tournament == tournament.ID, Results.ID_players == player.ID).count() > 0:
                        
                        #update tournament result of the given user and discipline DB...
                        result = session.query(Results).filter(Results.ID_discipline == d[1].ID, Results.ID_tournament == tournament.ID, Results.ID_players == player.ID)
                        #TODO: date changed does not work yet (update not possible due to not workingfunc.current_timestamp())
                        #.update({'DateChanged': (func.current_timestamp())})

                        #create the score entry and link it to the result entry in the DB...
                        score = session.query(Score).filter(Score.ID_result == result[0].ID).update({'Score': (form.score.data)})
#                        session.add(score)
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
#                form = OneVsOneDisciplineForm()

                #prepare/get table params...
                num_players = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_tournament == tournament.ID).count()
                print('There are %d players', num_players)

                #get table data from DB...
                #get all active players but current_user...
                opponents = session.query(TournamentsPlayersMap, Users).join(Users, (TournamentsPlayersMap.ID_users == Users.ID)).filter(Users.ID != current_user.ID, TournamentsPlayersMap.status == 'active')

                forms = []
                for o in opponents:
                    labelstring = 'Hast du gegen ' + o.Users.UserName + ' gewonnen?'
#                    f = OneVsOneEntryForm()
#                    f.result.label = labelstring
                    forms.append(OneVsOneEntryForm(prefix=o.Users.UserName))
                    forms[-1].result.label = labelstring

                for i, f in enumerate(forms):
                    if f.submit.data and f.validate_on_submit():
                        print(f.submit.data)
                        print(f.result.data)
                        print(opponents[i].Users.UserName)

                        #get player info of current user
                        player = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_users == current_user.ID).first()

                        #get player info of opponent
                        opp = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_users == opponents[i].Users.ID).first()


                        #
                        #Step1: create/modify match result of current_user 
                        #

                        #create tournament result of the given user and discipline DB (if not already exists)
                        if session.query(Results).filter(Results.ID_discipline == d[1].ID, Results.ID_tournament == tournament.ID, Results.ID_players == player.ID).count() == 0:
                            
                            result = Results(DateCreated=func.current_timestamp(), DateChanged=func.current_timestamp(), ID_discipline=d[1].ID, ID_tournament=tournament.ID, ID_players=player.ID)
                            session.add(result)
                            session.commit()
                        else:
                            result = session.query(Results).filter(Results.ID_discipline == d[1].ID, Results.ID_tournament == tournament.ID, Results.ID_players == player.ID)
                            result = result[0]

                        if session.query(MatchResult).filter(MatchResult.ID_result == result.ID, MatchResult.ID_players == opp.ID).count() == 0:
                            #create the match result entry and link it to the result entry in the DB...
                            print(result.ID)
                            matchresult = MatchResult(ID_result=result.ID, ID_players=opp.ID, match_result=f.result.data)
                            session.add(matchresult)
                            session.commit()
                            flash('User Result added!')
                        else:
                            #create the score entry and link it to the result entry in the DB...
                            matchresult = session.query(MatchResult).filter(MatchResult.ID_result == result.ID, MatchResult.ID_players == opp.ID).update({'match_result': (f.result.data)})
#                            session.add(matchresult)
                            session.commit()
                            flash('User Result modified!')

                        #
                        #Step2: create/modify match result of opponent of current_user
                        #

                        #create tournament result of the opponent user and discipline DB (if not already exists)
                        if session.query(Results).filter(Results.ID_discipline == d[1].ID, Results.ID_tournament == tournament.ID, Results.ID_players == opp.ID).count() == 0:
                            
                            oppresult = Results(DateCreated=func.current_timestamp(), DateChanged=func.current_timestamp(), ID_discipline=d[1].ID, ID_tournament=tournament.ID, ID_players=opp.ID)
                            session.add(oppresult)
                            session.commit()
                        else:
                            oppresult = session.query(Results).filter(Results.ID_discipline == d[1].ID, Results.ID_tournament == tournament.ID, Results.ID_players == opp.ID)
                            oppresult = oppresult[0]

                        #ATTENTION: for the opponent, the match_result needs to be inverted from f.result.data
                        if f.result.data == 'win':
                            match_result_inverted = 'lose'
                        elif f.result.data == 'lose':
                            match_result_inverted = 'win'
                        else:
                            match_result_inverted = 'none'

                        if session.query(MatchResult).filter(MatchResult.ID_result == oppresult.ID, MatchResult.ID_players == player.ID).count() == 0:
                            #create the match result entry and link it to the result entry in the DB...
                            print(oppresult.ID)
                            oppmatchresult = MatchResult(ID_result=oppresult.ID, ID_players=player.ID, match_result=match_result_inverted)
                            session.add(oppmatchresult)
                            session.commit()
                            flash('Opponent Result added!')
                        else:
                            #create the score entry and link it to the result entry in the DB...
                            oppmatchresult = session.query(MatchResult).filter(MatchResult.ID_result == oppresult.ID, MatchResult.ID_players == player.ID).update({'match_result': (match_result_inverted)})
#                            session.add(oppmatchresult)
                            session.commit()
                            flash('Opponent Result modified!')

                
                return render_template('discipline_one_vs_one.html', current_user=current_user, discipline=d, forms=forms, opponents=opponents)

    return "Record not found", 400

@app.route('/disciplines/results')
@login_required
def results():
    tournament = session.query(Tournaments).order_by(desc(Tournaments.Season)).first()
    if tournament is not None:
        disciplinelist =  session.query(TournamentsDisciplinesMap, Disciplines).join(Disciplines, (TournamentsDisciplinesMap.ID_discipline == Disciplines.ID)).filter(TournamentsDisciplinesMap.ID_tournament == tournament.ID)
    else:
        disciplinelist = None
        return render_template('results.html', current_user=current_user, disciplinelist=disciplinelist)  

    #get table data from DB...
    num_players = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_tournament == tournament.ID, TournamentsPlayersMap.status == 'active').count()
    print('There are %d players', num_players)
    players = session.query(TournamentsPlayersMap, Users).join(Users, (TournamentsPlayersMap.ID_users == Users.ID)).filter(TournamentsPlayersMap.ID_tournament == tournament.ID, TournamentsPlayersMap.status == 'active').order_by(asc(Users.UserName))

    #initialize total ressults with 0
    totalresults = [0] * num_players
    totalresults = list(map(list, zip(players, totalresults)))

    for d in disciplinelist:
        if d[1].type == 'Single':
            
            #get table data from DB...
            results = session.query(Results, Score, TournamentsPlayersMap, Users).join(Score, (Score.ID_result == Results.ID)).join(TournamentsPlayersMap, (Results.ID_players == TournamentsPlayersMap.ID)).join(Users, (TournamentsPlayersMap.ID_users == Users.ID)).filter(Results.ID_discipline == d[1].ID).order_by(asc(Score.Score))

            if results is not None:
                for i, r in enumerate(results):

                    #find the user in totalresults list
                    for player in totalresults:
                        if player[0].Users.ID == r[3].ID:
                            player[1] = player[1] + i + 1

        elif d[1].type == 'OneVsOne':
            
            matrix = []
            totals = []
            for row, p in enumerate(players):
                column = []
                total = 0
                for col, o in enumerate(players):
                    if o == p:
                        column.append('n/a')
                    else:
                        result = session.query(Results, MatchResult).join(MatchResult, (Results.ID == MatchResult.ID_result)).filter(Results.ID_players == p[0].ID, MatchResult.ID_players == o[0].ID).first()
                        if result is not None:
                            if result[1].match_result == 'win':
                                column.append('1')
                                total = total + 1
                            elif result[1].match_result == 'lose':
                                column.append('0')
                            else:
                                column.append('')
                        else: 
                            column.append('')
                matrix.append(column)
                totals.append(total)

            disciplineresults = list(zip(players, totals))
            print(disciplineresults)

            disciplineresults = sorted(disciplineresults, key=lambda disciplineresults:disciplineresults[1])

            for i, r in enumerate(disciplineresults):

                #find the user in totalresults list
                for player in totalresults:
                    if player[0].Users.ID == r[0].Users.ID:
                        player[1] = player[1] + i + 1


    totalresults = sorted(totalresults, key=lambda totalresults:totalresults[1], reverse=True)

    return render_template('results.html', current_user=current_user, disciplinelist=disciplinelist, totalresults=totalresults)


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
                results = session.query(Results, Score, TournamentsPlayersMap, Users).join(Score, (Score.ID_result == Results.ID)).join(TournamentsPlayersMap, (Results.ID_players == TournamentsPlayersMap.ID)).join(Users, (TournamentsPlayersMap.ID_users == Users.ID)).filter(Results.ID_discipline == d[1].ID, TournamentsDisciplinesMap.ID_tournament == tournament.ID, TournamentsPlayersMap.status == 'active').order_by(desc(Score.Score))

                return render_template('result_discipline_single.html', current_user=current_user, discipline=d, num_players=num_players, results=results)
            elif d[1].type == 'OneVsOne':
                #get table data from DB...
                num_players = session.query(TournamentsPlayersMap).filter(TournamentsPlayersMap.ID_tournament == tournament.ID, TournamentsPlayersMap.status == 'active').count()
                print('There are %d players', num_players)
                players = session.query(TournamentsPlayersMap, Users).join(Users, (TournamentsPlayersMap.ID_users == Users.ID)).filter(TournamentsPlayersMap.ID_tournament == tournament.ID, TournamentsPlayersMap.status == 'active').order_by(asc(Users.UserName))

                matrix = []
                totals = []
                for row, p in enumerate(players):
                    column = []
                    total = 0
                    for col, o in enumerate(players):
                        if o == p:
                            column.append('n/a')
                        else:
                            result = session.query(Results, MatchResult).join(MatchResult, (Results.ID == MatchResult.ID_result)).filter(Results.ID_players == p[0].ID, MatchResult.ID_players == o[0].ID).first()
                            if result is not None:
                                if result[1].match_result == 'win':
                                    column.append('1')
                                    total = total + 1
                                elif result[1].match_result == 'lose':
                                    column.append('0')
                                else:
                                    column.append('')
                            else: 
                                column.append('')
                    matrix.append(column)
                    totals.append(total)

                disciplineresults = list(zip(players, totals))
                print(disciplineresults)

                disciplineresults = sorted(disciplineresults, key=lambda disciplineresults:disciplineresults[1], reverse=True)

                return render_template('result_discipline_one_vs_one.html', current_user=current_user, discipline=d, players=players, matrix=matrix, disciplineresults=disciplineresults)

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
