from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View
from django import forms

from racepoint.models import Point


class Main(View):
	login_form = None
	error = False
	
	def get(self, request):
		"""Handles the GET request."""
		if 'organiser' in request.session:
			return self.render_home(request)
		else:
			return self.render_login(request)
	
	def post(self, request):
		"""Handles the POST request."""
		self.login_form = self.LoginForm(request.POST)
		if self.login_form.is_valid():
			try:
				point = Point.objects.get(password=self.login_form.cleaned_data['password'])
			except (Point.DoesNotExist, Point.MultipleObjectsReturned):
				pass
			else:
				request.session['organiser'] = self.login_form.cleaned_data['name']
				request.session['point'] = point
				return self.render_home(request)
		self.error = True
		return self.render_login(request)
	
	def render_login(self, request):
		"""Renders the login form."""
		if self.login_form is None:
			self.login_form = self.LoginForm()
		return render_to_response(
			'racepoint/home/login.html',
			{
				'form': self.login_form,
				'error': self.error
			},
			context_instance = RequestContext(request)
		)
	
	def render_home(self, request):
		"""Renders home for logged in organisers."""
		return render_to_response(
			'racepoint/home/home.html',
			{},
			context_instance = RequestContext(request)
		)
	
	class LoginForm(forms.Form):
		name = forms.CharField(max_length=120)
		password = forms.CharField(max_length=120)


class Logout(View):
	def get(self, request):
		"""Handles the GET request."""
		if 'organiser' in request.session:
			del request.session['organiser']
		return HttpResponseRedirect('/')

