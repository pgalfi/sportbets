from rest_framework import serializers

from matchbets.models import Match, MatchMarket, Selection, Message, Sport


# Below are serializers configured for each model. Uses the inner Meta class to provide configuration information
# to Django Rest Framework on how to wire these up.
# The built-in validator for the unique ID on each model is disabled because the creation of these will be
# performed with by provide a create logic at the Message model level.

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ["id", "name"]
        extra_kwargs = {
            'id': {'validators': []},
        }


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name", "odds"]
        extra_kwargs = {
            'id': {'validators': []},
        }


class MatchMarketSerializer(serializers.ModelSerializer):
    selections = SelectionSerializer(many=True)

    class Meta:
        model = MatchMarket
        fields = ["id", "name", "selections"]
        extra_kwargs = {
            'id': {'validators': []},
        }


class MatchSerializer(serializers.ModelSerializer):
    markets = MatchMarketSerializer(many=True)
    sport = SportSerializer()

    class Meta:
        model = Match
        fields = ["id", "url", "name", "startTime", "sport", "markets"]
        extra_kwargs = {
            'id': {'validators': []},
        }


class MatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["id", "url", "name", "startTime"]


class MessageSerializer(serializers.ModelSerializer):
    event = MatchSerializer()

    class Meta:
        model = Message
        fields = ["id", "message_type", "event"]
        extra_kwargs = {
            'id': {'validators': []},
        }

    def create(self, validated_message_data):
        """Parse the validated incoming data for a new message and create all relevant objects.
        Check message type and create new objects only if called for."""

        is_new_event = validated_message_data["message_type"] == Message.NEWEVENT_TYPE

        validated_event_data = validated_message_data.pop("event")
        validated_markets_data = validated_event_data.pop("markets")

        sport, created = Sport.objects.get_or_create(**validated_event_data.pop("sport"))
        validated_event_data["sport"] = sport
        match, created = Match.objects.get_or_create(**validated_event_data)

        for market in validated_markets_data:
            selections = market.pop("selections")
            if is_new_event:
                market["match"] = match
                market = MatchMarket.objects.create(**market)
            for selection in selections:
                if is_new_event:
                    selection["market"] = market
                    Selection.objects.create(**selection)
                else:
                    try:
                        selection_object = Selection.objects.get(id=selection["id"])
                    except Selection.DoesNotExist:
                        raise serializers.ValidationError(detail="Requested selection with id={} does not exist"
                                                          .format(selection["id"]))
                    selection_object.odds = selection["odds"]
                    selection_object.save()

        validated_message_data["event"] = match
        event_message, created = Message.objects.get_or_create(**validated_message_data)
        return event_message
