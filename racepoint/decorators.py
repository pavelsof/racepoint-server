from django.http import HttpResponseNotFound


def require_organiser(decorated):
	"""Decorator for restricting access to authenticated organisers."""
	def __decorated(*args, **kwargs):
		request = args[0]
		if 'organiser' in request.session:
			return decorated(*args, **kwargs)
		else:
			return HttpResponseNotFound()
	return __decorated

