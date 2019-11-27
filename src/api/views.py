from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from gmusicapi import Mobileclient

from oauth2client.client import AccessTokenCredentials, OAuth2WebServerFlow, OAuth2Credentials

# Create your views here.
oauth = (
        '228293309116.apps.googleusercontent.com',
        'GL1YV0XMp0RlL7ylCV3ilFz-',
        'https://www.googleapis.com/auth/skyjam',
        'urn:ietf:wg:oauth:2.0:oob'
    )

class GetMusicListView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.POST.get('token')
        device_id = request.POST.get('device-id') or Mobileclient.FROM_MAC_ADDRESS



        flow = OAuth2WebServerFlow(client_id=oauth[0], client_secret=oauth[1], scope = oauth[2], redirect_uri=oauth[3])
        credentials = OAuth2Credentials(access_token=str(token), client_id=Mobileclient.FROM_MAC_ADDRESS, client_secret=oauth[1], refresh_token = str(token), token_expiry=None, token_uri="https://accounts.google.com/o/oauth2/token", user_agent="user-agent/1.0")
        





        mobile_client = Mobileclient()

        #credentials = AccessTokenCredentials(access_token = str(token), user_agent="user-agent/1.0")
        
        mobile_client.oauth_login(oauth_credentials=credentials, device_id=device_id)
        return Response(mobile_client.get_all_songs())

class GetPlaylistsView(APIView):
    def get(self, request, *args, **kwargs):

        user_email = request.POST.get("email")
        user_password = request.POST.get("password")
        android_id = request.POST.get("android-id")

        if android_id == None:
            android_id = Mobileclient.FROM_MAC_ADDRESS

        mobile_client = Mobileclient()

        if not mobile_client.login(email=user_email, password=user_password, android_id=android_id):
            return Response("LOGIN FAIL")

        return Response(mobile_client.get_all_playlists())

