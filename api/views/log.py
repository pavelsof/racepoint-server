from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from api.auth import authenticate_request
from api.models import LogEvent, Team
from api.views.utils import make_json, read_json

from datetime import datetime


class LogView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		"""
		Ensures the user has a valid token.
		"""
		try:
			self.token = authenticate_request(request)
		except ValueError:
			return HttpResponse(status=403)
		
		return super(LogView, self).dispatch(request, *args, **kwargs)
	
	def get(self, request):
		"""
		Returns the log events.
		"""
		events = LogEvent.objects.filter(
			point = self.token.point
		)
		
		response = []
		for event in events:
			response.append({
				'id': event.pk,
				'teamId': event.team.pk,
				'teamName': event.team.name,
				'type': event.event_type,
				'timestamp': int(event.timestamp.timestamp()*1000),
				'isSuccessful': event.is_successful
			})
		
		return HttpResponse(make_json(response), status=200)
	
	def put(self, request):
		"""
		Adds a log event.
		"""
		try:
			post_fields = read_json(request.body)
		except ValueError:
			return HttpResponse(_("JSON, please!"), status=400)
		
		try:
			assert type(post_fields['team_id']) is int
			assert type(post_fields['event_type']) is str
			assert post_fields['event_type'] in ('ARR', 'DEP')
			assert type(post_fields['timestamp']) is int
			assert type(post_fields['is_successful']) is bool
		except (AssertionError, KeyError):
			return HttpResponse(_("Hack attempt detected."), status=400)
		
		try:
			team = Team.objects.get(pk=post_fields['team_id'])
		except Team.DoesNotExist:
			return HttpResponse(_("Unrecognised team."), status=400)
		
		event = LogEvent()
		event.point = self.token.point
		event.team = team
		event.event_type = post_fields['event_type']
		event.timestamp = datetime.fromtimestamp(post_fields['timestamp']/1000.0)
		event.is_successful = post_fields['is_successful']
		event.save()
		
		response = {
			'id': event.pk
		}
		return HttpResponse(make_json(response), status=200)

