from django.urls import path

from .views import GetAuthorizationURI, GetTokens, GetSongsList, GetPlaylists


urlpatterns = [
    #path("login/", LoginView.as_view()),
    path("auth-url/", GetAuthorizationURI.as_view()),
    path("tokens/", GetTokens.as_view()),
    path("songs-list/", GetSongsList.as_view()),
    path("playlists/", GetPlaylists.as_view()),
]
