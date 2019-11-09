from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestMatchViewSet(TestCase):

    fixtures = ["test-data-set-1.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.maxDiff = 2048

    def test_match_01(self):
        match_endpoint = reverse("match-detail", args=[994839351740])
        response = self.client.get(match_endpoint, format="json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("Real Madrid vs Barcelona", response.data["name"])
        self.assertEqual("Winner", response.data["markets"][0]["name"])
        self.assertEqual(1.01, response.data["markets"][0]["selections"][0]["odds"])

    def test_match_02(self):
        match_endpoint = reverse("match-detail", args=[1111111])
        response = self.client.get(match_endpoint, format="json")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_match_list_01(self):
        match_endpoint = reverse("match-list")
        response = self.client.get(match_endpoint, data={"sport": "football", "ordering": "startTime"}, format="json", )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual("Real Madrid vs Barcelona", response.data[0]["name"])
        self.assertTrue("sport" not in response.data[0])

    def test_match_list_02(self):
        match_endpoint = reverse("match-list")
        response = self.client.get(match_endpoint, data={"name": "Real Madrid vs Barcelona"}, format="json", )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual("Real Madrid vs Barcelona", response.data[0]["name"])




