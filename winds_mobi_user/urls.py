from django.urls import path

from winds_mobi_user.views import Login, Profile, ProfileFavorite
from .facebook_views import FacebookOauth2Callback
from .google_views import GoogleOauth2Callback

app_name = 'user'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),

    path('profile/', Profile.as_view(), name='profile'),
    path('profile/favorites/<str:station_id>/', ProfileFavorite.as_view(), name='profile_favorites'),

    path('google/oauth2callback/', GoogleOauth2Callback.as_view(), name='google_oauth2callback'),
    path('facebook/oauth2callback/', FacebookOauth2Callback.as_view(), name='facebook_oauth2callback')
]
