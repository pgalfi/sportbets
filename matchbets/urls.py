from rest_framework import routers

from matchbets.api_views import MatchViewSet, MessageViewSet

# Wire and connect up the defined viewsets using the Router provided by Django Rest framework. It translates
# the defined and available API calls to URL routes automatically.

router = routers.SimpleRouter()
router.register(r'match', MatchViewSet)
router.register(r'message', MessageViewSet)

urlpatterns = router.urls