from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from ctf import views

urlpatterns = [
                  path('', views.scoreboard, name='scoreboard'),
                  path('challenges/', views.ChallengeIndexView.as_view(), name='challenge-index'),
                  path('challenges/<int:pk>/', views.ChallengeDetailView.as_view(), name='challenge-detail'),
                  path('challenges/<int:pk>/submit-flag/', views.submit_flag, name='submit-flag'),
                  path('logout/', LogoutView.as_view(), {'next_page': 'scoreboard'}, name='logout'),
                  path('login/', views.ctflogin, name='login'),
                  path('admin/', admin.site.urls),

              ] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
