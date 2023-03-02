from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
from django.shortcuts import redirect
from django.views import View
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from django.conf import settings


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "credImp.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection and REDIRECT URL.
SCOPES = [
          'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/userinfo.email',
          'openid'
          ]


API_VERSION = 'v3'

REDIRECT_URL = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'

API_SERVICE_NAME = 'calendar'



@api_view(['GET'])
def GoogleCalendarInitView(request):
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = REDIRECT_URL

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    request.session['state'] = state

    return Response({"authorization_url": authorization_url})

def credentials_to_dict(credentials):
  return {
          'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes
          }



@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    # Specify the state parameter to prevent CSRF attacks.
    state = request.session['state'] if 'state' in request.session else None

    # Fetch the authorization response.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URL
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # Get the credentials and store them in the session.
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    # Use the credentials to get the user's calendar events.
    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Return the calendar events.
    return Response({'events': events})
