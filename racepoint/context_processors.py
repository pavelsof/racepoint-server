def populate_context(request):
	"""Populates the context with the app's global variables."""
	context = {}
	if 'racepoint_session' in request.session:
		session = request.session['racepoint_session']
		context['username'] = session.username
	else:
		context['username'] = ''
	return context

