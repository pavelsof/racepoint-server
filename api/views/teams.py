from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from api.auth import authenticate_request
from api.models import Team, Player
from api.views.utils import make_json, read_json


class TeamsView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		"""
		Ensures the user has a valid token.
		"""
		try:
			self.token = authenticate_request(request)
		except ValueError:
			return HttpResponse(status=403)
		
		return super(TeamsView, self).dispatch(request, *args, **kwargs)
	
	def get(self, request):
		"""
		Returns the registered teams.
		"""
		teams = Team.objects.filter(
			race = self.token.race
		)
		
		response = []
		for team in teams:
			response.append({
				'id': team.pk,
				'name': team.name,
				'players': team.get_player_names()
			})
		
		return HttpResponse(make_json(response), status=200)
	
	def put(self, request):
		"""
		Adds a team.
		"""
		try:
			post_fields = read_json(request.body)
		except ValueError:
			return HttpResponse(_("JSON, please!"), status=400)
		
		try:
			assert type(post_fields['name']) is str
			assert type(post_fields['players']) is list
			for item in post_fields['players']:
				assert type(item) is str
		except (AssertionError, KeyError):
			return HttpResponse(_("Hack attempt detected."), status=400)
		
		team = Team()
		team.race = self.token.race
		team.name = post_fields['name']
		team.save()
		
		for player_name in post_fields['players']:
			player = Player()
			player.team = team
			player.name = player_name
			player.save()
		
		response = {
			'id': team.pk
		}
		return HttpResponse(make_json(response), status=200)
	
	def delete(self, request):
		"""
		Deletes a team.
		"""
		try:
			post_fields = read_json(request.body)
		except ValueError:
			return HttpResponse(_("JSON, please!"), status=400)
		
		try:
			assert type(post_fields['id']) is int
		except AssertionError:
			return HttpResponse(_("Hack attempt detected."), status=400)
		
		try:
			team = Team.objects.get(
				race = self.token.race,
				pk = post_fields['id']
			)
		except Team.DoesNotExist:
			return HttpResponse(_("No such team."), status=400)
		
		team.delete()
		return HttpResponse(status=200)

