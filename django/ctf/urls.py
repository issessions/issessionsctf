from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings 

from .views import *

urlpatterns = [
    path('', scoreboard, name='scoreboard'),
    path('challenges/', ChallengeIndexView.as_view(), name='challenge-index'),
    path('challenges/<int:pk>/', ChallengeDetailView.as_view(), name='challenge-detail'),
    path('challenges/<int:pk>/submit-flag/', submit_flag, name='submit-flag'),
    path('logout/', LogoutView.as_view(), {'next_page': 'scoreboard'}, name='logout'),
    path('login/', ctflogin, name='login'),
    path('download/<str:minio_bucket>/<str:minio_file_id>/', download, name='ctf-download'),
    path('sponsors/',sponsors,name='sponsors'),
    path('change_password/',change_password, name='Change Password'),
    path('team_management/',team_management,name='Team Management'),
    path('challenges/<int:pk>/reveal-hint/',reveal_hint, name='reveal-hint'),
    path('help/tutorials', help_tutorials, name='tutorials'),
    path('help/tools', help_tools, name='tool'),
    path('help/other', help_other, name='other'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)