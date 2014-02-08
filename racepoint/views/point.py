from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View
from django import forms

from racepoint.models import TeamAtPoint


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
		teams_here = []
		teams_left = []
		teams_at_this_point = TeamAtPoint.objects.filter(
			point = self.point,
			departure__isnull = True
		).order_by('arrival')
		for team_at_point in teams_at_this_point:
			teams_here.append({
				'name': team_at_point.team.name,
				'arrival': team_at_point.arrival
			})
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
				'teams_here': teams_here,
				'teams_left': teams_left
			},
			context_instance = RequestContext(request)
		)


class Add(PointView):
	def get(self, request):
		"""Handles the GET request."""
		pass
	
	def post(self, request):
		"""Handles the POST request."""
		pass

