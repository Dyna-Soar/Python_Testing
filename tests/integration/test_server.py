import pytest
from server import app


def test_purchase_places_and_point_display():
    club_name = "Simply Lift"
    points = "13"
    competition_name = "Spring Festival"
    places_available = "25"
    reserved_places = 2

    client = app.test_client()

    response = client.post("/purchasePlaces", {"club": club_name, "competition": competition_name})
    assert response.status_code == 200

    response = client.get("/point-display")
    assert response.status_code == 200
    assert b"Simply Lift has 7 points" in response.data

