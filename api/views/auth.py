from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.base import View

from api.models import AuthToken, Race, Point
from api.views.utils import make_json, read_json

from datetime import date


class AuthView(View):
	def post(self, request):
		"""
		Makes a token corresponding to the key submitted.
		"""
		try:
			post_fields = read_json(request.body)
		except ValueError:
			return HttpResponse(_("JSON, please!"), status=400)
		
		try:
			assert type(post_fields['role']) is str
			assert type(post_fields['password']) is str
			assert post_fields['password']
		except (AssertionError, KeyError):
			return HttpResponse(_("Hack attempt detected."), status=400)
		
		token = AuthToken()
		
		if post_fields['role'] == 'LOG':
			try:
				point = Point.objects.get(
					password = post_fields['password'],
					race__date__gte = date.today()
				)
			except Point.DoesNotExist:
				return HttpResponse(_("Unrecognised password."), status=400)
			token.race = point.race
			token.point = point
			token.role = 'LOG'
		
		elif post_fields['role'] == 'REG':
			try:
				race = Race.objects.get(
					password = post_fields['password'],
					date__gte = date.today(),
				)
			except Race.DoesNotExist:
				return HttpResponse(_("Unrecognised password."), status=400)
			token.race = race
			token.role = 'REG'
		
		else:
			return HttpResponse(_("Unrecognised role."), status=400)
		
		token.save()
		
		response = {
			'token': token.token
		}
		return HttpResponse(make_json(response), status=200)

