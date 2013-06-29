##
# Automaintenance.  Django app to track automaintenance records.
# Copyright (C) 2012 Robert Robinson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns

from gplus_signin.views import ErrorView, LoginView, AuthView

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(),
        name='gplus_signin'),

    # Car Records
    url(r'^auth/$',
        AuthView.as_view(),
        name='gplus_auth'),
    url(r'^error/$',
        ErrorView.as_view(),
        name='gplus_error'),
                       
)
