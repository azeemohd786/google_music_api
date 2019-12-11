from django.urls import path

from .views import ReturnNothing, GetAuthorizationURI, GetTokens, GetSongsList, GetPlaylists


urlpatterns = [
    #path("login/", LoginView.as_view()),
    path("", ReturnNothing.as_view()), # Change this to return all availible endpoints.
    path("auth-url/", GetAuthorizationURI.as_view()),
    path("tokens/", GetTokens.as_view()),
    path("songs-list/", GetSongsList.as_view()),
    path("playlists/", GetPlaylists.as_view()),
]
