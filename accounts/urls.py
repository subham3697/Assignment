from .views import *
from django.urls import re_path
from django.contrib import admin


admin.autodiscover()

app_name = 'accounts'

urlpatterns = [
    re_path(r'^$', web_login, name='web_login'),
    re_path(r'^$', log_out_view, name='web_logout_view'),
    re_path(r'^signup/$', web_signup, name='web_signup'),

    re_path(r'^/$', blog_list, name='blog_list'),

]