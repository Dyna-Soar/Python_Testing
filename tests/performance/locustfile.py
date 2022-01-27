from locust import HttpUser, task
from server import loadCompetitions


class PerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("")

    @task
    def showSummary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Spring Festival/Iron Temple")

    @task
    def purchasePlaces(self):
        self.client.post("/purchasePlaces", {'competition': "Fall Classic", 'club': "She Lifts", 'places': 1})

    @task
    def point_display(self):
        self.client.get("/point-display")
