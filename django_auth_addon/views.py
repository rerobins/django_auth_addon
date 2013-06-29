# Create your views here.

from django.views.generic import TemplateView
from apiclient.discovery import build
import httplib2
import json
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from django.conf import settings


SERVICE = build('plus', 'v1')

class ErrorView(TemplateView):
    template_name = "gplus_signin/error.html"
    

class LoginView(TemplateView):
    template_name = "gplus_signin/login.html"
    

class AuthView(TemplateView):
    template_name = "gplus_signin/auth.html"
    
    def get_context_data(self, **kwargs):
        """
            Add the command type to the maintenance view for display.
        """
        context = super(AuthView, self).get_context_data(**kwargs)

        context['result'] = self.result
        context['tokeninfo'] = self.tokeninfo
        context['access_code'] = self.access_code
        context['access_token'] = self.credentials.access_token
               
        return context
    
    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """

        self.access_code = self.request.POST['access_code'] 
        
        oauth_flow = flow_from_clientsecrets(settings.CLIENT_SECRETS, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        self.credentials = oauth_flow.step2_exchange(self.access_code)
#         # Upgrade the authorization code into a credentials object
# #         FLOW.redirect_uri = 'postmessage'
# #         credentials = FLOW.step2_exchange(self.access_code)
#         # Create a new authorized API client.
        http = httplib2.Http()
        http = self.credentials.authorize(http)
        # Get a list of people that this user has shared with this app.
        google_request = SERVICE.people().get(userId='me')
        self.result = google_request.execute(http=http)
    
        access_token = self.credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
                 % access_token)
        h = httplib2.Http()
        self.tokeninfo = json.loads(h.request(url, 'GET')[1])
            
        return super(AuthView, self).get(request, *args, **kwargs)    
