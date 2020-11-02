
from django.conf.urls import url
from . import views

app_name = 'cal'
urlpatterns = [
	url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]