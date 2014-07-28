from django.test import TestCase
from django.test.client import Client

from api.models import *
from api.tests.factory import *

from datetime import datetime, timedelta


class AuthTestCase(TestCase):
	def test_post(self):
		client = Client()
		
		# no body
		response = client.post('/api/auth/', content_type="application/octet-stream")
		self.assertEqual(response.status_code, 400)
		
		# no password
		body = '{"role":"REG"}'
		response = client.post('/api/auth/', body, content_type="application/octet-stream")
		self.assertEqual(response.status_code, 400)
		
		# empty password
		body = '{"password": "", "role":"REG"}'
		response = client.post('/api/auth/', body, content_type="application/octet-stream")
		self.assertEqual(response.status_code, 400)
	
	def test_post_REG(self):
		race = RaceFactory.produce()
		client = Client()
		
		# good key
		tokens_before = AuthToken.objects.count()
		body = '{"password": "'+race.password+'", "role":"REG"}'
		response = client.post('/api/auth/', body, content_type="application/octet-stream")
		self.assertEqual(response.status_code, 200)
		tokens_after = AuthToken.objects.count()
		self.assertEqual(tokens_after, tokens_before+1)
		
		token = AuthToken.objects.latest('expiration')
		self.assertEqual(token.race.pk, race.pk)
		self.assertEqual(token.role, 'REG')
		
		# wrong password
		body = '{"password": "'+race.password[:-1]+'", "role":"REG"}'
		response = client.post('/api/auth/', body, content_type="application/octet-stream")
		self.assertEqual(response.status_code, 400)
		
		# past races
		race.date = datetime.now() - timedelta(days=1)
		race.save()
		body = '{"password": "'+race.password+'", "role":"REG"}'
		response = client.post('/api/auth/', body, content_type="application/octet-stream")
		self.assertEqual(response.status_code, 400)
	
	def test_post_LOG(self):
		race = RaceFactory.produce()
		point = PointFactory.produce(race)
		client = Client()
		
		# good key
		tokens_before = AuthToken.objects.count()
		body = '{"password": "'+point.password+'", "role":"LOG"}'
		response = client.post('/api/auth/', body, content_type="application/octet-stream")
		self.assertEqual(response.status_code, 200)
		tokens_after = AuthToken.objects.count()
		self.assertEqual(tokens_after, tokens_before+1)
		
		token = AuthToken.objects.latest('expiration')
		self.assertEqual(token.race.pk, race.pk)
		self.assertEqual(token.point.pk, point.pk)
		self.assertEqual(token.role, 'LOG')
		
		# wrong password
		body = '{"password": "'+point.password[:-1]+'", "role":"LOG"}'
		response = client.post('/api/auth/', body, content_type="application/octet-stream")
		self.assertEqual(response.status_code, 400)
		
		# past races
		race.date = datetime.now() - timedelta(days=1)
		race.save()
		body = '{"password": "'+point.password+'", "role":"LOG"}'
		response = client.post('/api/auth/', body, content_type="application/octet-stream")
		self.assertEqual(response.status_code, 400)

