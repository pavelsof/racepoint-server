from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from api.models import AuthToken, Race, Point
from api.views.utils import make_json, read_json

from datetime import date


class AuthView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		"""
		Applies the csrf_exempt decorator.
		"""
		return super(AuthView, self).dispatch(request, *args, **kwargs)
	
	def post(self, request):
		"""
		Makes a token corresponding to the key submitted.
		"""
		try:
			post_fields = read_json(request.body)
		except ValueError:
			return HttpResponse(_("JSON, please!"), status=400)
		
		try:
			assert type(post_fields['password']) is str
			assert post_fields['password']
		except (AssertionError, KeyError):
			return HttpResponse(_("Hack attempt detected."), status=400)
		
		try:
			token = self.make_log_token(post_fields['password'])
		except ValueError:
			try:
				token = self.make_reg_token(post_fields['password'])
			except ValueError:
				return HttpResponse(_("Unrecognised password."), status=400)
		token.save()
		
		response = {
			'token': token.token,
			'role': token.role
		}
		return HttpResponse(make_json(response), status=200)
	
	def make_log_token(self, password):
		"""
		Returns LOG-type token or raises ValueError.
		"""
		token = AuthToken()
		
		try:
			point = Point.objects.get(
				password = password,
				race__date__gte = date.today()
			)
		except Point.DoesNotExist:
			raise ValueError
		
		token.race = point.race
		token.point = point
		token.role = 'LOG'
		
		return token
	
	def make_reg_token(self, password):
		"""
		Returns REG-type token or raises ValueError.
		"""
		token = AuthToken()
		
		try:
			race = Race.objects.get(
				password = password,
				date__gte = date.today(),
			)
		except Race.DoesNotExist:
			raise ValueError
		
		token.race = race
		token.role = 'REG'
		
		return token

