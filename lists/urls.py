from django.conf.urls import patterns, url
from .views import new_list, view_list, my_lists, share_list

urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$', view_list, name='view_list'),
    url(r'^(?P<pk>\d+)/share/$', share_list, name='share_list'),
    url(r'^new$', new_list, name='new_list'),
    url(r'^users/(?P<email>.+)/$', my_lists, name='my_lists'),
)
