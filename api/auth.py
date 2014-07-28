from api.models import AuthToken

import time


def authenticate_request(request):
	"""
	Returns AuthToken or raises ValueError.
	"""
	if 'HTTP_RACEPOINT_TOKEN' not in request.META:
		raise ValueError
	
	try:
		token = AuthToken.objects.get(pk=request.META['HTTP_RACEPOINT_TOKEN'])
	except AuthToken.DoesNotExist:
		raise ValueError
	
	if int(time.time()) > token.expiration:
		raise ValueError
	
	return token

