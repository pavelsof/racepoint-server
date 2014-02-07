from django.db import models


class Race(models.Model):
	"""One for each game/race/hunt/adventure."""
	name = models.CharField(max_length=120)
	date = models.DateField()
	
	def __str__(self):
		return self.name


class Point(models.Model):
	"""One for each checkpoint of each race."""
	name = models.CharField(max_length=120)
	race = models.ForeignKey(Race)
	password = models.CharField(max_length=120)
	
	def __str__(self):
		return self.name


class Team(models.Model):
	"""One for each team in each race."""
	name = models.CharField(max_length=120)
	race = models.ForeignKey(Race)
	
	def __str__(self):
		return self.name


class Player(models.Model):
	"""One for each player in each team in each race."""
	name = models.CharField(max_length=120)
	team = models.ForeignKey(Team)
	
	def __str__(self):
		return self.name


class Event(models.Model):
	"""One for each happening of interest."""
	ARRIVAL = 'arr'
	DEPARTURE = 'dep'
	type = models.CharField(
		max_length=3,
		choices=(
			(ARRIVAL, 'Arrival'),
			(DEPARTURE, 'Departure'),
		)
	)
	time = models.TimeField()
	point = models.ForeignKey(Point)
	team = models.ForeignKey(Team)
	players = models.ManyToManyField(Player)
	
	def __str__(self):
		return self.type + ': ' + self.point + ': ' + self.team

