from rest_framework import viewsets

from .models import Activity, LeaderboardEntry, Team, TrackerUser, Workout
from .serializers import (
    ActivitySerializer,
    LeaderboardEntrySerializer,
    TeamSerializer,
    TrackerUserSerializer,
    WorkoutSerializer,
)


class BaseCollectionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']


class TeamViewSet(BaseCollectionViewSet):
    queryset = Team.objects.all().order_by('name', 'id')
    serializer_class = TeamSerializer


class TrackerUserViewSet(BaseCollectionViewSet):
    queryset = TrackerUser.objects.select_related('team').all().order_by('hero_alias', 'id')
    serializer_class = TrackerUserSerializer


class ActivityViewSet(BaseCollectionViewSet):
    queryset = Activity.objects.select_related('user').all().order_by('-performed_at', '-id')
    serializer_class = ActivitySerializer


class LeaderboardEntryViewSet(BaseCollectionViewSet):
    queryset = LeaderboardEntry.objects.select_related('user').all().order_by('rank', '-points')
    serializer_class = LeaderboardEntrySerializer


class WorkoutViewSet(BaseCollectionViewSet):
    queryset = Workout.objects.select_related('user').all().order_by('title', 'id')
    serializer_class = WorkoutSerializer