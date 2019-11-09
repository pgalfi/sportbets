from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from matchbets.models import Message, Selection, Match


class TestMessageViewSet(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.endpoint = reverse("message-list")
        self.maxDiff = 4096

    def test_messages_01(self):
        """Test a new event being created"""

        message_data = {
            "id": 8661032861909884224,
            "message_type": "NewEvent",
            "event": {
                "id": 994839351740,
                "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20T10:30:00",
                "sport": {
                    "id": 221,
                    "name": "Football"
                },
                "markets": [
                    {
                        "id": 385086549360973392,
                        "name": "Winner",
                        "selections": [
                            {
                                "id": 8243901714083343527,
                                "name": "Real Madrid",
                                "odds": 1.01
                            },
                            {
                                "id": 5737666888266680774,
                                "name": "Barcelona",
                                "odds": 1.01
                            }
                        ]
                    }
                ]
            }
        }
        response = self.client.post(self.endpoint, message_data, format="json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Message.objects.filter(pk=8661032861909884224).count())
        self.assertEqual(1, Match.objects.filter(pk=994839351740).count())
        self.assertEqual(1.01, Selection.objects.filter(pk=8243901714083343527)[0].odds)

    def test_messages_02(self):
        """Test an update against non-existent event."""

        message_data = {
            "id": 8661032861909884224,
            "message_type": "UpdateOdds",
            "event": {
                "id": 994839351740,
                "name": "Real Madrid vs Barcelona",
                "startTime": "2018-06-20T10:30:00",
                "sport": {
                    "id": 221,
                    "name": "Football"
                },
                "markets": [
                    {
                        "id": 385086549360973392,
                        "name": "Winner",
                        "selections": [
                            {
                                "id": 8243901714083343527,
                                "name": "Real Madrid",
                                "odds": 2
                            },
                            {
                                "id": 5737666888266680774,
                                "name": "Barcelona",
                                "odds": 1.01
                            }
                        ]
                    }
                ]
            }
        }
        response = self.client.post(self.endpoint, message_data, format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

