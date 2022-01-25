import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    global clubs
    global competitions

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Redirect to booking if the club is trying to purchase too many places(12)
    if placesRequired > 12:
        flash(f'You tried to purchase {placesRequired} places. Only 12 places per competitions are available.')
        return render_template('booking.html',club=club,competition=competition)

    # Redirect to booking if the club has purchased places in the competition and is trying to purchase too many places(12)
    if "competitions" in club:
        if competition["name"] in club["competitions"]:
            if placesRequired + club["competitions"][competition["name"]]["places"] > 12:
                flash(f'You tried to purchase {placesRequired} places. You already have {club["competitions"][competition["name"]]["places"]} places. Only 12 places per competitions are available.')
                return render_template('booking.html', club=club, competition=competition)

    # Find the index of the club in clubs data
    club_index = 0
    for i in range(len(clubs)):
        if clubs[i]["name"] == club["name"]:
            club_index = i
            break

    # if competitions data exist in club data, update that data
    if "competitions" in clubs[club_index]:
        # if the club already has booked places, update the number of places
        if competition["name"] in clubs[club_index]["competitions"]:
            clubs[club_index]["competitions"][competition["name"]]["places"] -= int(placesRequired)

        # if the club has never purchased places for this competition
        else:
            data_competition = {"places": placesRequired}
            clubs[club_index]["competitions"][competition["name"]] = data_competition

    # if the club has never purchased any place create a competitons dict with the places data
    else:
        competitions_dict = {}
        data_competition = {"places": placesRequired}
        competitions_dict[competition["name"]] = data_competition
        clubs[club_index]["competitions"] = competitions_dict

    # Update points
    clubs[club_index]["points"] = int(clubs[club_index]["points"]) - 3*placesRequired

    # Find the index of the competition in competitions data
    competition_index = 0
    for i in range(len(competitions)):
        if competitions[i]["name"] == competition["name"]:
            competition_index = i
            break

    # update the competition's places
    competitions[competition_index]['numberOfPlaces'] = int(competitions[competition_index]['numberOfPlaces']) - placesRequired

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))