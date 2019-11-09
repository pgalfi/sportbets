from django.db import models



class Sport(models.Model):
    """Data model: Each sport type has a name."""

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=2048)

    def __str__(self):
        return self.name


class Match(models.Model):
    """Data model: Many Matches -> one Sport"""

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=2048)
    startTime = models.DateTimeField()
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MatchMarket(models.Model):
    """Data model: Many MatchMarkets -> one Match

    A market is a kind of bet that can be made on the match."""

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=2048)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="markets")

    def __str__(self):
        return self.name + " of " + self.match.name


class Selection(models.Model):
    """Data model: Many Selections -> one MarketMatch

    A selection is a player that a bet can be placed on. A bet is a 'Market' for a 'Match'"""

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=2048)
    market = models.ForeignKey(MatchMarket, on_delete=models.CASCADE, related_name="selections")
    odds = models.FloatField()

    def __str__(self):
        return self.name + " - " + str(self.market) + " (odds: " + str(self.odds) + ")"


class Message(models.Model):
    """Data model: Message to process information from external providers"""

    NEWEVENT_TYPE = "NewEvent"
    UPDATEODDS_TYPE = "UpdateOdds"
    MESSAGE_TYPES = (
        (NEWEVENT_TYPE, "New Event"),
        (UPDATEODDS_TYPE, "Update Odds")
    )

    id = models.BigIntegerField(primary_key=True)
    message_type = models.CharField(max_length=1024, choices=MESSAGE_TYPES)
    event = models.ForeignKey(Match, null=True, default=None, on_delete=models.SET_NULL)
