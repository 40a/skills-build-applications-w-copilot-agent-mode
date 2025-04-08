from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import HttpResponseRedirect
from .views import UserViewSet, TeamViewSet, ActivityViewSet, LeaderboardViewSet, WorkoutViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'leaderboards', LeaderboardViewSet)
router.register(r'workouts', WorkoutViewSet)

urlpatterns = [
    path('', lambda request: HttpResponseRedirect('/api/')),
    path('api/', include(router.urls)),
]
