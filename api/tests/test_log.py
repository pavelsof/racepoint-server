from django.test import TestCase
from django.test.client import Client

from api.models import *
from api.tests.factory import *
from api.views.utils import read_json

from datetime import datetime
from time import time

import pytz
import random


class LogTestCase(TestCase):
	def test_get(self):
		race = RaceFactory.produce()
		for i in range(random.randrange(1,33)):
			TeamFactory.produce(race)
		
		point = PointFactory.produce(race)
		LogEventFactory.mass_produce(point)
		
		client = Client()
		token = AuthTokenFactory.produce(point)
		
		# no token
		response = client.get('/api/log/')
		self.assertEqual(response.status_code, 403)
		
		# alles gut
		response = client.get('/api/log/', HTTP_RACEPOINT_TOKEN=token.token)
		self.assertEqual(response.status_code, 200)
		events_ = read_json(response.content)
		self.assertEqual(len(events_), LogEvent.objects.filter(point=point).count())
	
	def test_put(self):
		race = RaceFactory.produce()
		point = PointFactory.produce(race)
		team = TeamFactory.produce(race)
		
		client = Client()
		token = AuthTokenFactory.produce(point)
		
		# no token
		response = client.put('/api/log/')
		self.assertEqual(response.status_code, 403)
		
		# good input
		# d = now()
		# timestamp = int(mktime(d.timetuple()))*1000
		t = int(time()*1000)
		d = datetime.fromtimestamp(t/1000.0)
		d = d.replace(tzinfo=pytz.UTC)
		timestamp = t
		body = ('{"team_id":'+ str(team.pk) +','
				' "event_type":"ARR",'
				' "timestamp":'+ str(timestamp) +','
				' "is_successful":false}')
		response = client.put('/api/log/', body, HTTP_RACEPOINT_TOKEN=token.token)
		self.assertEqual(response.status_code, 200)
		
		event = LogEvent.objects.latest('created')
		self.assertEqual(event.point.pk, point.pk)
		self.assertEqual(event.event_type, 'ARR')
		self.assertEqual(event.timestamp, d)
		self.assertEqual(event.is_successful, False)
		body = read_json(response.content)
		self.assertEqual(event.pk, body['id'])

