from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from matchbets.models import Message, Selection, Match, Sport


class TestMessageViewSet(TestCase):
    """Test with one event preloaded from fixture."""

    fixtures = ["test-data-set-1.json"]

    def setUp(self) -> None:
        self.client = APIClient()
        self.endpoint = reverse("message-list")
        self.maxDiff = 4096

    def test_messages_03(self):
        """Add one more event, same Sport as the one that exists."""

        message_data = {
            "id": 8661032861909884112,
            "message_type": "NewEvent",
            "event": {
                "id": 994839351745,
                "name": "FC Madrid vs Juventus",
                "startTime": "2018-06-20T10:31:00",
                "sport": {
                    "id": 221,
                    "name": "Football"
                },
                "markets": [
                    {
                        "id": 385086549360973393,
                        "name": "Winner",
                        "selections": [
                            {
                                "id": 8243901714083343577,
                                "name": "FC Madrid",
                                "odds": 1.01
                            },
                            {
                                "id": 5737666888266680441,
                                "name": "Juventus",
                                "odds": 1.5
                            }
                        ]
                    }
                ]
            }
        }
        response = self.client.post(self.endpoint, message_data, format="json")
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            self.assertEqual("", str(response.data))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Message.objects.filter(pk=8661032861909884112).count())
        self.assertEqual(1, Match.objects.filter(pk=994839351745).count())
        self.assertEqual(1.01, Selection.objects.filter(pk=8243901714083343577)[0].odds)
        # Check that only one Sport exists (Football)
        self.assertEqual(1, Sport.objects.all().count())
        self.assertEqual(2, Match.objects.all().count())


    def test_messages_04(self):
        """Update odds of preloaded event"""

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
                                "odds": 12
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
        # self.assertEqual("", str(response.data))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(12.0, Selection.objects.get(pk=8243901714083343527).odds)





