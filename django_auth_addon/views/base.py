
from django.views.generic import FormView

from django_auth_addon.views.forms import FullUserCreationForm

class CreateUser(FormView):
    template_name = 'django_auth_addon/create_user.html'
    form_class = FullUserCreationForm
    success_url = '/thanks/'



