from django.conf.urls import patterns, include, url

from racepoint.views import init
from racepoint.views import teams
from racepoint.views import point


urlpatterns = patterns('',
	url(r'^$', init.Main.as_view()),
	url(r'^logout/$', init.Logout.as_view()),
	url(r'^teams/$', teams.List.as_view()),
	url(r'^teams/add/$', teams.Add.as_view()),
	url(r'^point/$', point.Main.as_view()),
	url(r'^point/ajax/$', point.Ajax.as_view()),
)


