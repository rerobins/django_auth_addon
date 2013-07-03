
from django.contrib.auth.models import User
from django.db import models


class GooglePlusCredentialsModel(models.Model):
    """
    Bookkeeping field that will maintain information about credentials (needed for look up calls) and
    a pointer to the actual Django object that will be used to represent the user.
    """
    gplus_id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User)

