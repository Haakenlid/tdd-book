from django.conf.urls import patterns, url
from .views import new_list, view_list, my_lists

urlpatterns = patterns(
    '',
    url(r'^(\d+)/$', view_list, name='view_list'),
    url(r'^new$', new_list, name='new_list'),
    url(r'^users/(.+)/$', my_lists, name='my_lists'),
)