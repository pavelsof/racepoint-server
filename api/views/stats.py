from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from api.auth import authenticate_request
from api.models import LogEvent, Point, Team
from api.views.utils import make_json


class StatsView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		"""
		Ensures the user has a valid token.
		"""
		try:
			self.token = authenticate_request(request)
		except ValueError:
			return HttpResponse(status=403)
		
		return super(StatsView, self).dispatch(request, *args, **kwargs)
	
	def get(self, request):
		"""
		Returns some race stats.
		"""
		teams = Team.objects.filter(race=self.token.race)
		points_count = Point.objects.filter(race=self.token.race).count()
		response = []
		
		for team in teams:
			response_item = {
				'teamId': team.pk,
				'teamName': team.name,
				'log': [],
				'pointsBehind': 0,
				'pointsAhead': 0
			}
			points_behind = set()
			
			events = LogEvent.objects.filter(
				team = team
			).order_by('-timestamp')
			for event in events:
				points_behind.add(event.point)
				response_item['log'].append({
					'pointName': str(event.point),
					'eventType': event.event_type,
					'timestamp': event.timestamp
				})
			
			response_item['pointsBehind'] = len(points_behind)
			response_item['pointsAhead'] = points_count - len(points_behind)
			
			response.append(response_item)
		
		return HttpResponse(make_json(response), status=200)

