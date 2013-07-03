# Create your views here.
from django.core.urlresolvers import reverse

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


class ErrorView(TemplateView):
    template_name = "django_auth_addon/gplus/error.html"
    

class LoginView(TemplateView):
    template_name = "django_auth_addon/gplus/login.html"
    

class AuthView(TemplateView):
    template_name = ""

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.access_code = self.request.POST['access_code']

        user = authenticate(access_code=self.access_code)

        if user is None:
            return HttpResponseRedirect(reverse('gplus_error'))

        login(self.request, user)

        return HttpResponseRedirect(reverse('logged_in'))
