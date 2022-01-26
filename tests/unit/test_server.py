import pytest
from server import loadClubs, loadCompetitions
from server import app


def test_loadClubs():
    """Test the loadClubs function successfully loads clubs data"""
    clubs = loadClubs()
    assert clubs[0]["name"] == "Simply Lift"
    assert clubs[1]["email"] == "admin@irontemple.com"
    assert clubs[2]["points"] == "12"


def test_loadCompetitions():
    """Test the loadCompetitions function succesfully loads competitions data"""
    competitions = loadCompetitions()
    assert competitions[0]["name"] == "Spring Festival"
    assert competitions[1]["numberOfPlaces"] == "13"


def test_index_route():
    """Test the index route renders the index template"""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_showSummary_route():
    """Test the summary route renders welcome template with user's credentials"""
    email = "john@simplylift.co"
    client = app.test_client()
    response = client.post("/showSummary", data={'email': email})
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data


def test_wrong_showSummary_route():
    """Test the summary route with unknown credentials returns the index template"""
    email = "wrong@email.co"
    client = app.test_client()
    response = client.post("/showSummary", data={'email': email})
    assert response.status_code == 200
    assert b"Unknown email. Please enter the club's email." in response.data
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data


def test_book_route():
    """Test the book route renders book template with the competition and club's informations"""
    client = app.test_client()
    competition = "Fall Classic"
    club = "Simply Lift"
    response = client.get(f"/book/{competition}/{club}")
    assert response.status_code == 200
    assert b'Booking for Fall Classic' in response.data


def test_wrong_book_route():
    """Test the book route with unknown competition render the welcome template"""
    client = app.test_client()
    competition = "Unknown competition"
    club = "She Lifts"
    response = client.get(f"/book/{competition}/{club}")
    assert response.status_code == 200
    assert b'Something went wrong-please try again' in response.data


def test_purchasePlaces_route():
    """
    Test the purchasePlaces route updates clubs places
    Expect 3 points for 1 place
    """
    competition = 'Spring Festival'
    club = 'Simply Lift'
    places = '2'
    client = app.test_client()
    response = client.post("/purchasePlaces", data={'competition': competition, 'club': club, 'places': places})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    from server import clubs
    assert int(clubs[0]["competitions"]["Spring Festival"]["places"]) == 2


def test_toomuch_purchasePlaces_route():
    """The user tries to book more places than the 12 limit"""
    competition = 'Spring Festival'
    club = 'Simply Lift'
    places = '13'
    client = app.test_client()
    response = client.post("/purchasePlaces", data={'competition': competition, 'club': club, 'places': places})
    assert response.status_code == 200
    assert b'You tried to purchase 13 places. Only 12 places per competitions are available.' in response.data
    assert b'Booking for Spring Festival' in response.data


def test_notenough_purchasePlaces_route():
    """
    The user try to buy more places than he has points
    Expect 3 points for 1 place
    In this test case the club has 10 points
    """
    competition = 'Spring Festival'
    club = 'Simply Lift'
    # The club has 10 points
    places = 5
    client = app.test_client()
    response = client.post("/purchasePlaces", data={'competition': competition, 'club': club, 'places': places})
    assert response.status_code == 200
    assert b'You are trying to buy 5 places. One place costs 3 points. You only have 10 points.' in response.data
    assert b'Booking for Spring Festival' in response.data
    from server import competitions
    assert int(competitions[0]["numberOfPlaces"]) != int(competitions[0]["numberOfPlaces"]) - places


def test_point_display():
    """Test the point-display route renders the index with with current points of clubs"""
    client = app.test_client()
    response = client.get("/point-display")
    assert b"Simply Lift has 10 points" in response.data
    assert b"Iron Temple has 4 points" in response.data
    assert b"She Lifts has 12 points" in response.data


def test_logout():
    """Test logout route redirects to index"""
    client = app.test_client()
    response = client.get("/logout")
    assert response.status_code == 302
