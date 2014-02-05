from django.shortcuts import render_to_response
from django.template import RequestContext


def show_home(request):
	return render_to_response(
		'racepoint/home/home.html',
		{},
		context_instance = RequestContext(request)
	)


def list_teams(request):
	return render_to_response(
		'racepoint/base.html',
		{},
		context_instance = RequestContext(request)
	)


def add_team(request):
	return render_to_response(
		'racepoint/base.html',
		{},
		context_instance = RequestContext(request)
	)


def list_points(request):
	return render_to_response(
		'racepoint/base.html',
		{},
		context_instance = RequestContext(request)
	)


def add_point(request):
	return render_to_response(
		'racepoint/base.html',
		{},
		context_instance = RequestContext(request)
	)


def show_point(request):
	return render_to_response(
		'racepoint/base.html',
		{},
		context_instance = RequestContext(request)
	)


def add_event(request):
	return render_to_response(
		'racepoint/base.html',
		{},
		context_instance = RequestContext(request)
	)


