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
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired


    # Club file update part
    # Update number of places and points values by opening clubs json file
    clubs_data = None
    with open("clubs.json", "r") as clubs_file:
        clubs_data = json.load(clubs_file)

        # Find the index of the club in the json data
        club_index = 0
        for i in range(len(clubs_data["clubs"])):
            if clubs_data["clubs"][i]["name"] == club["name"]:
                club_index = i
                break

        clubs_data["clubs"][club_index]["points"] -= placesRequired
        # if the competition already has data in competition, it updates it
        if clubs_data["clubs"][club_index]["competitions"][competition["name"]]:
            places_already_purchased = int(clubs_data["clubs"][club_index]["competitions"][competition["name"]]["places_purchased"])
            clubs_data["clubs"][club_index]["competitions"][competition["name"]]["places_purchased"] = places_already_purchased + placesRequired

        # if competitions data exist but not for this competition
        elif clubs_data["clubs"][club_index]["competitions"]:
            data_competition = {"places_purchased": places_required}
            clubs_data["clubs"][club_index]["competitions"][competition["name"]] = data_competition

        ## if no data it create it, with a list of dictionaries of commpetitions with name and place purchased
        else:
            competitions_dict = {}
            data_competition = {"places_purchased": placesRequired}
            competitions_dict[competition["name"]] = data_competition
            clubs_data["clubs"][club_index]["competitions"] = competitions_dict

        clubs_file.close()

    # Update the values in the clubs json file
    with open("clubs.json", "w") as clubs_file:
        clubs_file.write(json.dumps(clubs_data))
        clubs_file.close()


    # Competition file update
    # Update places available value by opening the json file
    competitions_data = None
    with open("competitions.json", "r") as competitions_file:

        competitions_data = json.load(competitions_file)

        # Find the index of the competition in the json data
        competition_index = 0
        for i in range(len(competitions_data)):
            if competition_data["competitions"][i]["name"] == competition["name"]:
                competition_index = i
                break

        numberOfPlaces = int(competitions_data["competitions"][competition_index]["numberOfPlaces"])
        competitions_data["competitions"][competition_index]["numberOfPlaces"] = numberOfPlaces - placesRequired


    # Update the values in the competitions json file
    with open("competitions.json", "w") as competitions_file:
        competitions_file.write(json.dumps(competitions_data))
        competitions_file.close()


    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))