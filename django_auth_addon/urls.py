
from django.conf.urls import url, patterns

from django_auth_addon.views.google_plus import ErrorView, LoginView, AuthView

from django_auth_addon.views.base import CreateUser

urlpatterns = patterns('',

    url(r'^gplus/$', LoginView.as_view(),   name='gplus_signin'),

    # Car Records
    url(r'^gplus/auth/$', AuthView.as_view(), name='gplus_auth'),
    url(r'^gplus/error/$', ErrorView.as_view(), name='gplus_error'),


    url(r'^create_user/$', CreateUser.as_view(), name='create_user'),
)
