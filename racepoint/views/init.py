from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.views.generic.base import View
from django import forms

from racepoint.models import Password
from racepoint.models import Session


class Main(View):
	form = None
	error = False
	
	def get(self, request):
		"""Handles the GET request."""
		if 'racepoint_session' in request.session:
			return self.render_home(request)
		else:
			return self.render_login(request)
	
	def post(self, request):
		"""Handles the POST request."""
		self.form = self.LoginForm(request.POST)
		if self.form.is_valid():
			password = Password.objects.filter(
				password = self.form.cleaned_data['password'],
				valid_from__lt = timezone.now(),
				valid_until__gt = timezone.now()
			)
			print(password)
			if password:
				session = Session()
				session.password = password[0]
				session.username = self.form.cleaned_data['name']
				session.last_seen = timezone.now()
				session.save()
				request.session['racepoint_session'] = session
				return self.render_home(request)
		self.error = True
		return self.render_login(request)
	
	def render_login(self, request):
		"""Renders the login form."""
		if self.form is None:
			self.form = self.LoginForm()
		return render_to_response(
			'racepoint/home/login.html',
			{
				'form': self.form,
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
		"""Form for authenticating organisers."""
		name = forms.CharField(max_length=120)
		password = forms.CharField(max_length=120)


class Logout(View):
	def get(self, request):
		"""Handles the GET request."""
		if 'racepoint_session' in request.session:
			del request.session['racepoint_session']
		return HttpResponseRedirect('/')

