from django.test import TestCase
from django.test.client import Client

from api.models import *
from api.tests.factory import *
from api.views.utils import read_json

from datetime import datetime, timedelta

import random


class TeamsTestCase(TestCase):
	def test_get(self):
		race = RaceFactory.produce()
		for i in range(random.randrange(1,33)):
			TeamFactory.produce(race)
		
		client = Client()
		token = AuthTokenFactory.produce(race)
		
		# no token
		response = client.get('/api/teams/')
		self.assertEqual(response.status_code, 403)
		
		# alles gut
		response = client.get('/api/teams/', HTTP_RACEPOINT_TOKEN=token.token)
		self.assertEqual(response.status_code, 200)
		teams_ = read_json(response.content)
		self.assertEqual(len(teams_), Team.objects.filter(race=race).count())
	
	def test_put(self):
		race = RaceFactory.produce()
		
		client = Client()
		token = AuthTokenFactory.produce(race)
		
		# no token
		response = client.put('/api/teams/')
		self.assertEqual(response.status_code, 403)
		
		# bad input
		body = '{"players":["One", "Two", "Three", "Four"]}'
		response = client.put('/api/teams/', body, HTTP_RACEPOINT_TOKEN=token.token)
		self.assertEqual(response.status_code, 400)
		
		# good input
		body = '{"name":"New Team", "players":["One", "Two", "Three", "Four"]}'
		response = client.put('/api/teams/', body, HTTP_RACEPOINT_TOKEN=token.token)
		self.assertEqual(response.status_code, 200)
		
		team_ = Team.objects.latest('created')
		self.assertEqual(team_.name, 'New Team')
		self.assertEqual(team_.get_player_names(), ["One", "Two", "Three", "Four"])
		body = read_json(response.content)
		self.assertEqual(team_.pk, body['id'])
	
	def test_delete(self):
		race = RaceFactory.produce()
		team = TeamFactory.produce(race)
		another_race = RaceFactory.produce()
		another_team = TeamFactory.produce(another_race)
		count_teams = Team.objects.count()
		
		client = Client()
		token = AuthTokenFactory.produce(race)
		
		# no token
		response = client.delete('/api/teams/')
		self.assertEqual(response.status_code, 403)
		
		# token for another race
		body = '{"id":'+ str(another_team.pk) +'}'
		response = client.delete('/api/teams/', body, HTTP_RACEPOINT_TOKEN=token.token)
		self.assertEqual(response.status_code, 400)
		
		# good input
		body = '{"id":'+ str(team.pk) +'}'
		response = client.delete('/api/teams/', body, HTTP_RACEPOINT_TOKEN=token.token)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Team.objects.count(), count_teams-1)

