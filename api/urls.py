from django.conf.urls import patterns, include, url
from django.views.decorators.http import require_http_methods

from api.views.auth import AuthView
from api.views.log import LogView
from api.views.stats import StatsView
from api.views.teams import TeamsView


urlpatterns = patterns('',
	url(r'auth/$', require_http_methods(['OPTIONS', 'POST'])(AuthView.as_view())),
	url(r'log/$', require_http_methods(['OPTIONS', 'GET', 'PUT', 'DELETE'])(LogView.as_view())),
	url(r'teams/$', require_http_methods(['OPTIONS', 'GET', 'PUT', 'DELETE'])(TeamsView.as_view())),
	url(r'stats/$', require_http_methods(['OPTIONS', 'GET'])(StatsView.as_view())),
)

"""
POST /auth/
	password
	200: token, role
	400: error

GET /teams/
	200: list of {id, name, players}
	403

PUT /teams/
	name, players
	200: id
	400: error
	403

DELETE /teams/
	team_id
	200
	400: error
	403

GET /log/
	200: list of {id, teamId, teamName, type, timestamp, isSuccessful}
	403

PUT /log/
	team_id, event_type, timestamp, is_successful
	200: id
	400: error
	403

DELETE /log/
	event_id
	200
	400: error
	403

GET /stats/
	200: list of {teamId, teamName, log: list of {pointName, eventType, timestamp}, pointsBehind, pointsAhead}
	403
"""
