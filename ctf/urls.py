from django.contrib.auth.views import LogoutView
from django.urls import path

from ctf.views import *

urlpatterns = [
    path('', scoreboard, name='scoreboard'),
    path('challenges/', ChallengeIndexView.as_view(), name='challenge-index'),
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge-detail'),
    path('challenges/<int:pk>/submit-flag/', submit_flag, name='submit-flag'),
    path('logout/', LogoutView.as_view(), {'next_page': 'scoreboard'}, name='logout'),
    path('login/', ctflogin, name='login'),
]
