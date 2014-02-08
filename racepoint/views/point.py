from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View
from django import forms

from racepoint.models import Player
from racepoint.models import Team
from racepoint.models import TeamAtPoint

import json


class PointView(View):
	point = None
	
	def dispatch(self, request, *args, **kwargs):
		"""Requires authentication."""
		if 'racepoint_session' not in request.session:
			raise Http404
		if not request.session['racepoint_session'].password.point:
			raise Http404
		self.point = request.session['racepoint_session'].password.point
		return super(PointView, self).dispatch(request, *args, **kwargs)


class Main(PointView):
	def get(self, request):
		"""Handles the GET request."""
		all_teams = Team.objects.filter(
			race = self.point.race
		).order_by('name')
		teams_here = []
		teams_at_this_point = TeamAtPoint.objects.filter(
			point = self.point,
			departure__isnull = True
		).order_by('arrival')
		for team_at_point in teams_at_this_point:
			teams_here.append({
				'name': team_at_point.team.name,
				'arrival': team_at_point.arrival
			})
		teams_left = []
		teams_left_this_point = TeamAtPoint.objects.filter(
			point = self.point,
			departure__isnull = False
		).order_by('arrival')
		for team_at_point in teams_left_this_point:
			teams_left.append({
				'name': team_at_point.team.name,
				'arrival': team_at_point.arrival,
				'departure': team_at_point.departure
			})
		return render_to_response(
			'racepoint/point/main.html',
			{
				'all_teams': all_teams,
				'teams_here': teams_here,
				'teams_left': teams_left
			},
			context_instance = RequestContext(request)
		)


class Ajax(PointView):
	def post(self, request):
		"""AJAX is POST only."""
		task = request.POST['task']
		if task == 'get_players': return self.get_players(request)
		elif task == 'add_arrival': return self.add_arrival(request)
	
	def get_players(self, request):
		"""Renders the contents of the select players modal."""
		try:
			team_id = int(request.POST['team'])
		except ValueError:
			return HttpResponseBadRequest('')
		try:
			team = Team.objects.get(pk=team_id)
		except Team.DoesNotExist:
			return HttpResponseBadRequest('')
		players = Player.objects.filter(team=team)
		return render_to_response(
			'racepoint/point/select_players.html',
			{
				'players': players
			},
			context_instance = RequestContext(request)
		)
	
	def add_arrival(self, request):
		"""Adds a new arrival to the db and gives a JSON answer."""
		try:
			team_id = int(request.POST['team'])
		except ValueError: return HttpResponseBadRequest('')
		try:
			team = Team.objects.get(pk=team_id)
		except Team.DoesNotExist: return HttpResponseBadRequest('')
		players = []
		for i in request.POST.getlist('players[]'):
			try:
				player_id = int(i)
			except ValueError: return HttpResponseBadRequest('')
			try:
				player = Player.objects.get(pk=player_id)
			except Player.DoesNotExist: return HttpResponseBadRequest('')
			players.append(player_id)
		team_at_point = TeamAtPoint()
		team_at_point.team = team
		team_at_point.point = self.point
		team_at_point.registered_by = self.request.session['racepoint_session']
		team_at_point.save()
		team_at_point.players = players
		team_at_point.save()
		answer = True
		return HttpResponse(json.dumps(answer))

