from rest_framework import viewsets, mixins

from matchbets.api_serializers import *
from matchbets.models import Match, Message


class MatchViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Set of API calls on the Match model providing listing and retrieval actions."""

    queryset = Match.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return MatchListSerializer
        elif self.action == "retrieve":
            return MatchSerializer
        return MatchSerializer

    def get_queryset(self):
        """Build queryset object that will be used to retrieve data from the backend, apply any query parameters
        as filters and if individual match is being retrieved then include all related objects to be retrieved from
        the backend most efficiently."""

        qs = Match.objects.all()
        if self.action == "list":
            sport_param = self.request.query_params.get("sport", None)
            ordering = self.request.query_params.get("ordering", None)
            name = self.request.query_params.get("name", None)
            # If no search parameters are provided that returns empty list
            if not(sport_param or name):
                return Match.objects.none()
            if sport_param:
                qs = qs.filter(sport__name__iexact=sport_param)
            if name:
                qs = qs.filter(name__iexact=name)
            if ordering:
                qs = qs.order_by(ordering)

        elif self.action == "retrieve":
            # Set up queryset to prefetch all related information that the serializer will need to return in as few
            # queries as possible
            qs = qs.select_related("sport").prefetch_related("markets", "markets__selections")
        return qs

    # Temporary override of dispatch to look at backend queries executed on the backend for optimization
    # def dispatch(self, request, *args, **kwargs):
    #     response = super().dispatch(request, *args, **kwargs)
    #     print(connection.queries)
    #     print(len(connection.queries))
    #     return response


class MessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """API call configuration for Message object creation. Automatically provides a response on the OPTIONS verb
    returning a json description of what the endpoint is expecting."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
