from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from apiclient.discovery import build
import httplib2
import json
from uuid import uuid4
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from django.conf import settings
from django.template.defaultfilters import slugify
from django_auth_addon.models import GooglePlusCredentialsModel


SERVICE = build('plus', 'v1')


class GooglePlusBackend(ModelBackend):

    def authenticate(self, access_code=None):

        if access_code is None:
            return None

        try:
            oauth_flow = flow_from_clientsecrets(settings.CLIENT_SECRETS, scope='')
            oauth_flow.redirect_uri = 'postmessage'
            self.credentials = oauth_flow.step2_exchange(access_code)
        except FlowExchangeError:
            return None

        # Check that the access token is valid.
        access_token = self.credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])

        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            return None

        access_token = self.credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
                 % access_token)
        h = httplib2.Http()
        token_info = json.loads(h.request(url, 'GET')[1])

        # http = httplib2.Http()
        # http = self.credentials.authorize(http)
        # # Get a list of people that this user has shared with this app.
        # google_request = SERVICE.people().get(userId='me')
        # people_document = google_request.execute(http=http)
        # context['given_name'] = self.people_document['name']['givenName']
        # context['family_name'] = self.people_document['name']['familyName']

        # Check to see if there is a google plus credential object with the provided user id from google

        google_plus_credentials = GooglePlusCredentialsModel.objects.filter(gplus_id=token_info['user_id'])

        if len(google_plus_credentials) == 0:
            credentials = GooglePlusCredentialsModel()
            credentials.gplus_id = token_info['user_id']

            # Need to create a whole new user object and move on.
            user = User.objects.create_user(get_username(), token_info['email'])

            credentials.user = user
            user.save()
            credentials.save()

        else:
            # Check to see if the credentials object has a user and then return it.
            user = google_plus_credentials[0].user

        return user


def get_username():
    max_length = 30

    username = slugify(uuid4().get_hex()[:max_length])
    while not is_valid_username(username):
        username = slugify(uuid4().get_hex()[:max_length])

    return username


def is_valid_username(username):
    if username is None:
        return False

    user_list = User.objects.filter(username=username)

    return len(user_list) == 0
