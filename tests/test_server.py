import pytest
from server import loadClubs, loadCompetitions
from server import app
from flask import Flask,render_template,request,redirect,flash,url_for, session

# fixture part

import os
import tempfile

#from flaskr import create_app
#from flaskr.db import init_db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    #app = create_app({'TESTING': True, 'DATABASE': db_path})
    app = Flask(__name__)
    app.config.from_pyfile({'TESTING': True, 'DATABASE': db_path})

    #with app.test_client() as client:
    #    with app.app_context():
    #        init_db()
    #    yield client

    os.close(db_fd)
    os.unlink(db_path)

    return tempfile.mkstemp()


# 11 tests unitaires


def test_loadClubs():
    clubs = loadClubs()
    assert len(clubs) != 0


def test_loadCompetitions():
    competitions = loadCompetitions()
    assert len(competitions) != 0


def test_index_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_showSummary_route():
    """Post request"""
    email = "john@simplylift.co"
    client = app.test_client()
    response = client.post("/showSummary", data={'email': email})
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data

def test_wrong_showSummary_route():
    email = "wrong@email.co"
    client = app.test_client()
    bad_response = client.post("/showSummary", data={'email': email})
    assert b"Wrong Email" in bad_response.data


def test_book_route():
    client = app.test_client()
    competition = "Spring Festival"
    club = "Simply Lift"
    url = f"/book/{competition}/{club}"
    response = client.get(url)
    assert response.status_code == 200
    assert b'Booking for Spring Festival' in response.data


def test_wrong_book_route():
    client = app.test_client()
    competition = "Unknown competition"
    club = "Unknown club"
    url = f"/book/{competition}/{club}"
    bad_response = client.get(url)
    assert bad_response.status_code == 200
    assert b'Something went wrong-please try again' in bad_response.data
    assert b'Welcome Unknown club' in bad_response.data

    # Make another test for good club, wrong competition

    # Make another test for wrong club, good competition


def test_purchasePlaces_route():
    """Post request"""
    competition = 'Spring Festival'
    club = 'Simply Lift'
    places = '2'
    fake_competition_places = 20
    fake_club_points = 10
    client = app.test_client()
    response = client.post("/purchasePlaces", data={'competition': competition, 'club': club, 'places': places})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert (fake_competition_places == fake_competition_places - int(places) and
            fake_club_points == fake_club_points - int(places))


def test_toomuch_purchasePlaces_route():
    """The user tries more places than the 12 limit"""
    competition = 'Spring Festival'
    club = 'Simply Lift'
    places = '13'
    fake_competition_places = 20
    fake_club_points = 15
    client = app.test_client()
    response = client.post("/purchasePlaces", data={'competition': competition, 'club': club, 'places': places})
    assert response.status_code == 200
    assert b'Only 12 places maximum for each club. You tried to buy 13 places.' in response.data


def test_notenough_purchasePlaces_route():
    """The user try to buy more places than he has points"""
    competition = 'Spring Festival'
    club = 'Simply Lift'
    places = '11'
    fake_competition_places = 20
    fake_club_points = 10
    client = app.test_client()
    response = client.post("/purchasePlaces", data={'competition': competition, 'club': club, 'places': places})
    assert response.status_code == 200
    assert b'You do not have enought points to buy 11 places. You currently have only 10 points' in response.data


"""
def test_login():
    email = "john@simplylift.co"
    client = app.test_client()
    response = client.post("/", data={'email': email})
    assert session['user'] == email
"""

"""
def test_bad_login():
    email = "error@simplylift.co"
    client = app.test_client()
    response = client.post("/", data={'email': email})
    assert response.data == "Wrong email"
"""

def test_logout():
    """Test logout"""
    email = "john@simplylift.co"
    client = app.test_client()
    response = client.post("/", data={'email': email})
    response = client.get("/logout")
    assert session['user'] == None
