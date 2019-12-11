from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from collections import namedtuple
import datetime
import requests
import json

from gmusicapi import Mobileclient

from oauth2client.client import OAuth2Credentials, OAuth2WebServerFlow

# Create your views here.

OAuthInfo = namedtuple('OAuthInfo', 'client_id client_secret scope redirect_uri')
oauth = {
        'client_id':'228293309116.apps.googleusercontent.com',
        'client_secret':'GL1YV0XMp0RlL7ylCV3ilFz-',
        'scope':'https://www.googleapis.com/auth/skyjam',
        'redirect_uri':'urn:ietf:wg:oauth:2.0:oob'
    }

class GetAuthorizationURI(APIView):
    def get(self, request, *args, **kwargs):
        auth_uri = "https://accounts.google.com/o/oauth2/v2/auth?client_id=228293309116.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fskyjam&access_type=offline&response_type=code"

        return Response({'auth-uri':auth_uri})

class GetTokens(APIView):
    def get(self, request, *args, **kwargs):
        
        code = request.headers['auth-code']
        print(code)
        if not code:
            return Response({'error':'no code'})
        
        flow = OAuth2WebServerFlow(client_id=oauth['client_id'], client_secret=oauth['client_secret'], scope=oauth['scope'], redirect_uri=oauth['redirect_uri'])
        credentials = flow.step2_exchange(code)

        return Response({'access-token':credentials.access_token, 'refresh-token':credentials.refresh_token})

class GetSongsList(APIView):
    def get(self, request, *args, **kwargs):
        token = request.headers['token']
        refresh_token = request.headers['refresh-token']

        expiry_response = requests.get("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}".format(token))

        remaining_time = json.loads(expiry_response.content)['expires_in']


        now = datetime.datetime.now()
        token_expiry = datetime.datetime.fromtimestamp(now.timestamp() + remaining_time)

        credentials = OAuth2Credentials(access_token=token, client_id=oauth['client_id'], client_secret=oauth['client_secret'], refresh_token=refresh_token, token_expiry=token_expiry,token_uri="https://www.googleapis.com/oauth2/v4/token", user_agent="user-agent/1.0")

        client = Mobileclient()
        if not client.oauth_login(device_id=Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=credentials):
            return Response({'error':'Login Failed'})
        
        return Response(client.get_all_songs())

class GetPlaylists(APIView):
    def get(self, request, *args, **kwargs):
        token = request.headers['token']
        refresh_token = request.headers['refresh-token']

        expiry_response = requests.get("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}".format(token))

        remaining_time = json.loads(expiry_response.content)['expires_in']


        now = datetime.datetime.now()
        token_expiry = datetime.datetime.fromtimestamp(now.timestamp() + remaining_time)

        credentials = OAuth2Credentials(access_token=token, client_id=oauth['client_id'], client_secret=oauth['client_secret'], refresh_token=refresh_token, token_expiry=token_expiry,token_uri="https://www.googleapis.com/oauth2/v4/token", user_agent="user-agent/1.0")

        client = Mobileclient()
        if not client.oauth_login(device_id=Mobileclient.FROM_MAC_ADDRESS, oauth_credentials=credentials):
            return Response({'error':'Login Failed'})
        
        return Response(client.get_all_playlists())