from locust import HttpUser, task
from server import loadCompetitions


class PerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("")

    @task
    def show_summary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def point_display(self):
        self.client.get("/point-display")
