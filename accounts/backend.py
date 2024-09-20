from .constants import *
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend



User = get_user_model()

class EmailLoginBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, role_id=None, **kwargs):
        try:
            user = User.objects.filter(Q(email=username)|Q(mobile_no=username)).last()
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user