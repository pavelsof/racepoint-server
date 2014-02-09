from django.utils import timezone


def populate_context(request):
	"""Populates the context with the app's global variables."""
	context = {}
	if 'racepoint_session' in request.session:
		session = request.session['racepoint_session']
		session.last_seen = timezone.now()
		session.save()
		context['username'] = session.username
		if session.password.point:
			context['race'] = session.password.point.race
		else:
			context['race'] = session.password.race
	else:
		context['username'] = ''
		context['race'] = ''
	return context

