from django.conf.urls import patterns, include, url

from racepoint.views import init
from racepoint.views import teams
from racepoint.views import point

from racepoint.decorators import require_organiser


urlpatterns = patterns('',
	url(r'^$', init.Main.as_view()),
	url(r'^logout/$', init.Logout.as_view()),
	url(r'^teams/$', require_organiser(teams.TeamsList.as_view())),
	url(r'^teams/add/$', require_organiser(teams.TeamsAdd.as_view())),
	url(r'^points/(?P<point_id>\d+)/$', point.main_view),
	url(r'^points/(?P<point_id>\d+)/add/$', point.add_event),
)

