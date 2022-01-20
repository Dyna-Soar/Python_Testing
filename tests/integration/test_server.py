import pytest
from server import loadClubs, loadCompetitions, showSummary, book, purchasePlaces, logout, point_display

def test_purchase_places_and_point_display():
    club_name = "Simply Lift"
    points = "13"
    competition_name = "Spring Festival"
    places_available = "25"
    reserved_places = 2

    client = app.test_client()
    response = client.post("/purchasePlaces", {"club": club_name, "competition": competition_name})
    response2 = client.get("/point-display")
    assert response.status_code == 200
    assert response2.status_code == 200
    assert b"Simply Lift has 7 points" in response2.data
