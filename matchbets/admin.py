from django.contrib import admin

from matchbets.models import Match, Sport, MatchMarket, Selection, Message

admin.site.register(Match)
admin.site.register(Sport)
admin.site.register(MatchMarket)
admin.site.register(Selection)
admin.site.register(Message)
