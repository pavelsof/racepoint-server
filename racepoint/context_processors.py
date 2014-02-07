def populate_context(request):
	"""Populates the context with the app's global variables."""
	context = {}
	if 'organiser' in request.session:
		context['organiser'] = request.session['organiser']
	else:
		context['organiser'] = ''
	return context

