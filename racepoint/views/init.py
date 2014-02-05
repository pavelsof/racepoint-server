from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms


request = None
login_form = None


def main_view(request_):
	"""This comes from urls.py."""
	global request
	request = request_
	if request.method == 'POST':
		handle_POST()
	if 'organiser' in request.session:
		return render_home()
	else:
		return render_login()


def handle_POST():
	"""Handles the login attempt."""
	return False


def render_login():
	"""Renders the login form."""
	return render_to_response(
		'racepoint/home/login.html',
		{
			'form': login_form
		},
		context_instance = RequestContext(request)
	)


def render_home():
	"""Renders home for logged in organisers."""
	return render_to_response(
		'racepoint/home/home.html',
		{},
		context_instance = RequestContext(request)
	)

