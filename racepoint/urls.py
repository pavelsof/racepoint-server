from django.conf.urls import patterns, include, url

from racepoint.views import init
from racepoint.views import teams
from racepoint.views import point


urlpatterns = patterns('',
	url(r'^$', init.Main.as_view()),
	url(r'^logout/$', init.Logout.as_view()),
	url(r'^teams/$', teams.list_all),
	url(r'^teams/add/$', teams.add_team),
	url(r'^points/(?P<point_id>\d+)/$', point.main_view),
	url(r'^points/(?P<point_id>\d+)/add/$', point.add_event),
)

