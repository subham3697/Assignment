from .views import *
from django.urls import re_path
from django.contrib import admin


admin.autodiscover()

app_name = 'blog'

urlpatterns = [
    re_path(r'^blog-details/(?P<id>\d+)/$', blog_detail, name='blog_detail'),
    re_path(r'^add-comment/(?P<id>\d+)/$', add_comment, name='add_comment'),
    re_path(r'like-blog/', like_blog, name='like_blog'),
    re_path(r'share-blog/', share_blog, name='share_blog'),

]