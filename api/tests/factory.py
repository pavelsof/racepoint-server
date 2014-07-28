from django.utils.timezone import now

from api.models import *

from datetime import datetime, timedelta

import random
import string


chars = string.ascii_letters + string.digits + ' '


class RaceFactory:
	def produce():
		race = Race()
		
		race.name = "".join(random.choice(chars) for i in range(random.randrange(1,60)))
		race.password = "".join(random.choice(chars) for i in range(random.randrange(1,33)))
		
		race.date = datetime.now()
		race.start = datetime.now() - timedelta(hours=2)
		race.end = datetime.now() + timedelta(hours=2)
		
		race.save()
		return race


class TeamFactory:
	def produce(race):
		team = Team()
		team.race = race
		team.name = "".join(random.choice(chars) for i in range(random.randrange(1,60)))
		team.save()
		
		for j in range(0, 4):
			player = Player()
			player.team = team
			player.name = "".join(random.choice(chars) for i in range(random.randrange(1,60)))
			player.save()
		
		return team


class PointFactory:
	def produce(race):
		point = Point()
		
		point.race = race
		point.name = "".join(random.choice(chars) for i in range(random.randrange(1,60)))
		point.password = "".join(random.choice(chars) for i in range(random.randrange(1,33)))
		
		point.save()
		return point


class LogEventFactory:
	def mass_produce(point):
		for team in Team.objects.filter(race=point.race):
			if random.randrange(0,2):
				continue
			for i in range(random.randrange(1,4)):
				arrival = LogEvent()
				arrival.point = point
				arrival.team = team
				arrival.timestamp = now() - timedelta(hours=i, minutes=5)
				arrival.save()
				departure = LogEvent()
				departure.point = point
				departure.team = team
				departure.timestamp = now() - timedelta(hours=i)
				departure.save()
			if random.randrange(0,2):
				arrival = LogEvent()
				arrival.point = point
				arrival.team = team
				arrival.timestamp = now() - timedelta(minutes=5)
				arrival.save()


class AuthTokenFactory:
	def produce(thing):
		token = AuthToken()
		
		if isinstance(thing, Race):
			token.race = thing
			token.role = 'REG'
		elif isinstance(thing, Point):
			token.race = thing.race
			token.point = thing
			token.role = 'LOG'
		else:
			raise ValueError
		
		token.save()
		return token

