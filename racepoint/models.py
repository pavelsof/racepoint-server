from django.db import models


class Race(models.Model):
	"""One for each game/race/hunt/adventure."""
	name = models.CharField(max_length=120)
	date = models.DateField()
	start = models.TimeField()
	end = models.TimeField()
	
	def __str__(self):
		return self.name


class Point(models.Model):
	"""One for each checkpoint of each race."""
	name = models.CharField(max_length=120)
	race = models.ForeignKey(Race)
	
	def __str__(self):
		return self.name


class Password(models.Model):
	"""At least one for each point and at least one for team registrars."""
	password = models.CharField(max_length=120, unique=True)
	race = models.ForeignKey(Race, blank=True, null=True)
	point = models.ForeignKey(Point, blank=True, null=True)
	valid_from = models.DateTimeField()
	valid_until = models.DateTimeField()
	
	def __str__(self):
		if self.point:
			return self.point.race.name +': '+ self.point.name
		elif self.race:
			return self.race.name +': Registration'
		else:
			return 'A useless password'


class Session(models.Model):
	"""One for each organiser login."""
	username = models.CharField(max_length=120)
	password = models.ForeignKey(Password)
	started = models.DateTimeField(auto_now_add=True)
	last_seen = models.DateTimeField()
	
	def __str__(self):
		return self.username +': '+ str(self.started)


class Team(models.Model):
	"""One for each team in each race."""
	name = models.CharField(max_length=120)
	race = models.ForeignKey(Race)
	registered_by = models.ForeignKey(Session)
	
	def __str__(self):
		return self.name


class Player(models.Model):
	"""One for each player in each team in each race."""
	name = models.CharField(max_length=120)
	team = models.ForeignKey(Team)
	
	def __str__(self):
		return self.name


class TeamAtPoint(models.Model):
	"""One for each team passing through a point."""
	team = models.ForeignKey(Team)
	point = models.ForeignKey(Point)
	arrival = models.TimeField(auto_now_add=True)
	departure = models.TimeField(blank=True, null=True)
	players = models.ManyToManyField(Player)
	registered_by = models.ForeignKey(Session)
	
	def __str__(self):
		return self.point.name + ': ' + self.team.name

