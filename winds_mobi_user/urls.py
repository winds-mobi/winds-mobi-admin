from django.urls import path

from winds_mobi_user.facebook_views import FacebookOauth2Callback
from winds_mobi_user.google_views import GoogleOauth2Callback
from winds_mobi_user.views import LoginView, ProfileFavoriteView, ProfileView

app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/favorites/<str:station_id>/', ProfileFavoriteView.as_view(), name='profile_favorites'),

    path('google/oauth2callback/', GoogleOauth2Callback.as_view(), name='google_oauth2callback'),
    path('facebook/oauth2callback/', FacebookOauth2Callback.as_view(), name='facebook_oauth2callback')
]
