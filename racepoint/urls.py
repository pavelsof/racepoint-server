from django.conf.urls import patterns, include, url

import racepoint.views

urlpatterns = patterns('',
	url(r'^$', racepoint.views.show_home),
	url(r'^teams/$', racepoint.views.list_teams),
	url(r'^teams/add/$', racepoint.views.add_team),
	url(r'^points/$', racepoint.views.list_points),
	url(r'^points/add/$', racepoint.views.add_point),
	url(r'^points/(?P<point_id>\d+)/$', racepoint.views.show_point),
	url(r'^points/(?P<point_id>\d+)/add/$', racepoint.views.add_event),
)
