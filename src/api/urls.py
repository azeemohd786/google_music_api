from django.urls import path

from .views import GetMusicListView, GetPlaylistsView


urlpatterns = [
    #path("login/", LoginView.as_view()),
    path("music-list/", GetMusicListView.as_view()),
    path("playlists-list/", GetPlaylistsView.as_view()),
]
