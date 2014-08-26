from django.http import HttpResponse


class CorsMiddleware:
	def process_request(self, request):
		"""
		Handles CORS preflight OPTIONS requests.
		"""
		if request.method == 'OPTIONS':
			if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
				response = HttpResponse(status=200)
				return response
		
		# django: None = go on
		return None
	
	def process_response(self, request, response):
		"""
		Enables CORS.
		"""
		if 'HTTP_ORIGIN' in request.META:
			response['Access-Control-Allow-Origin'] = "*"
			response['Access-Control-Allow-Methods'] = "GET, OPTIONS, PUT, DELETE"
			response['Access-Control-Allow-Headers'] = "Content-Type, Racepoint-Token, Origin"
			response['Access-Control-Max-Age'] = "86400"
		return response

