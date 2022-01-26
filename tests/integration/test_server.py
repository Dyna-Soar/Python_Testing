import pytest
from server import app, loadClubs, loadCompetitions


def test_purchase_places_and_point_display():
    """Test the purchase and the point display update correctly"""
    club_name = "Simply Lift"
    points = "13"
    competition_name = "Spring Festival"
    places_available = "25"
    reserved_places = 2

    client = app.test_client()

    response = client.post("/purchasePlaces", {"club": club_name, "competition": competition_name, 'places': reserved_places})
    assert response.status_code == 200

    response = client.get("/point-display")
    assert response.status_code == 200
    assert b"Simply Lift has 7 points" in response.data


def test_purchasing_places_by_different_clubs():
    """Test different clubs trying to purchase the places of the same competition"""

    clubs = loadClubs()
    assert clubs[0]["points"] == "13"
    assert clubs[1]["points"] == "4"
    assert clubs[2]["points"] == "12"

    import server
    server.competitions.append({"name": "Competition Test", "numberOfPlaces": "5"})

    from server import competitions
    assert competitions[2]["name"] == "Competition Test"
    assert competitions[2]["numberOfPlaces"] == "5"

    client = app.test_client()

    response = client.post("/purchasePlaces", data={"club": clubs[0]["name"], "competition": competitions[2]["name"], 'places': 4})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    response = client.post("/purchasePlaces", data={"club": clubs[1]["name"], "competition": competitions[2]["name"], 'places': 1})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    response = client.post("/purchasePlaces", data={"club": clubs[2]["name"], "competition": competitions[2]["name"], 'places': 1})
    assert response.status_code == 200


def test_every_function():
    """Test every function"""
    club_name = "Simply Lift"
    points = "13"

    client = app.test_client()

    clubs = loadClubs()
    assert clubs[0]["name"] == "Simply Lift"
    assert clubs[0]["email"] == "john@simplylift.co"
    assert clubs[0]["points"] == "13"

    competitions = loadCompetitions()
    assert competitions[0]["name"] == "Spring Festival"
    assert competitions[0]["numberOfPlaces"] == "25"
    assert competitions[1]["name"] == "Fall Classic"
    assert competitions[1]["numberOfPlaces"] == "13"

    response = client.get("/")
    assert response.status_code == 200

    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200

    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200

    response = client.post("/purchasePlaces", data={"competition": "Spring Festival", "club": "Simply Lift", "places": 4})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    response = client.post("/purchasePlaces", data={"competition": "Fall Classic", "club": "Simply Lift", "places": 1})
    assert response.status_code == 200
    assert b'You are trying to buy 1 places. One place costs 3 points. You only have 1 points.' in response.data

    response = client.get("/point-display")
    assert response.status_code
    assert b'Simply Lift has 1 points' in response.data

    response = client.get("/logout")
    assert response.status_code == 302
