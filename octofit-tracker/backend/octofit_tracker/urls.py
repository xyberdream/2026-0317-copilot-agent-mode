"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ActivityViewSet,
    LeaderboardEntryViewSet,
    TeamViewSet,
    TrackerUserViewSet,
    WorkoutViewSet,
)

codespace_name = os.environ.get('CODESPACE_NAME', '').strip()
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

router = DefaultRouter()
router.register('users', TrackerUserViewSet, basename='users')
router.register('teams', TeamViewSet, basename='teams')
router.register('activities', ActivityViewSet, basename='activities')
router.register('leaderboard', LeaderboardEntryViewSet, basename='leaderboard')
router.register('workouts', WorkoutViewSet, basename='workouts')

collection_paths = {
    'users': 'users',
    'teams': 'teams',
    'activities': 'activities',
    'leaderboard': 'leaderboard',
    'workouts': 'workouts',
}


def build_collection_url(collection):
    return f'{base_url}/api/{collection}/'


def api_root(_request):
    response_data = {'base_url': base_url}
    response_data.update(
        {name: build_collection_url(path) for name, path in collection_paths.items()}
    )
    return JsonResponse(response_data)

urlpatterns = [
    path('', api_root, name='root-api'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
