from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View
from django import forms

from racepoint.models import Team
from racepoint.models import Player


class Teams(View):
	def dispatch(self, request, *args, **kwargs):
		"""Requires authentication."""
		if 'racepoint_session' not in request.session:
			raise Http404
		if request.session['racepoint_session'].password.point:
			raise Http404
		return super(Teams, self).dispatch(request, *args, **kwargs)


class TeamsList(Teams):
	def get(self, request):
		"""Handles the GET request."""
		race = request.session['racepoint_session'].password.race
		teams = Team.objects.filter(race=race).order_by('name')
		for team in teams:
			team.players = Player.objects.filter(team=team)
		return render_to_response(
			'racepoint/teams/list.html',
			{
				'teams': teams
			},
			context_instance = RequestContext(request)
		)


class TeamsAdd(Teams):
	form = None
	
	def get(self, request):
		"""Handles the GET request."""
		self.form = self.RegistrationForm()
		return self.render(request)
	
	def post(self, request):
		"""Handles the POST request."""
		self.form = self.RegistrationForm(request.POST)
		if self.form.is_valid():
			team = Team()
			team.name = self.form.cleaned_data['team']
			team.race = request.session['point'].race
			team.save()
			for i in range(1, 5):
				if self.form.cleaned_data['player_'+str(i)]:
					player = Player()
					player.name = self.form.cleaned_data['player_'+str(i)]
					player.team = team
					player.save()
			return HttpResponseRedirect('/teams')
		return self.render(request)
	
	def render(self, request):
		"""Renders the template."""
		return render_to_response(
			'racepoint/teams/add.html',
			{
				'form': self.form
			},
			context_instance = RequestContext(request)
		)
	
	class RegistrationForm(forms.Form):
		"""Form for team registration."""
		team = forms.CharField(max_length=120)
		player_1 = forms.CharField(max_length=120)
		player_2 = forms.CharField(max_length=120, required=False)
		player_3 = forms.CharField(max_length=120, required=False)
		player_4 = forms.CharField(max_length=120, required=False)

