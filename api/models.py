from django.db import models
from django.utils.translation import ugettext_lazy as _

import time
import uuid


class Race(models.Model):
	name = models.CharField(max_length=240)
	date = models.DateField()
	start = models.TimeField()
	end = models.TimeField()
	password = models.CharField(max_length=32)
	
	def __str__(self):
		"""
		Returns the model's string representation.
		"""
		return self.name


class Team(models.Model):
	name = models.CharField(max_length=240)
	race = models.ForeignKey(Race)
	created = models.DateTimeField(auto_now_add=True)
	
	def get_player_names(self):
		"""
		Returns list of the players' names.
		"""
		names = []
		for player in Player.objects.filter(team=self):
			names.append(player.name)
		return names
	
	def __str__(self):
		"""
		Returns the model's string representation.
		"""
		return self.name


class Player(models.Model):
	name = models.CharField(max_length=240)
	team = models.ForeignKey(Team)
	
	def __str__(self):
		"""
		Returns the model's string representation.
		"""
		return self.name


class Point(models.Model):
	name = models.CharField(max_length=240)
	race = models.ForeignKey(Race)
	password = models.CharField(max_length=32)
	
	def __str__(self):
		"""
		Returns the model's string representation.
		"""
		return self.name


class LogEvent(models.Model):
	TYPES = (
		('ARR', _("Arrival")),
		('DEP', _("Departure"))
	)
	
	point = models.ForeignKey(Point)
	team = models.ForeignKey(Team)
	event_type = models.CharField(max_length=3, choices=TYPES)
	is_successful = models.BooleanField(default=False)
	timestamp = models.DateTimeField()
	created = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['timestamp']
		get_latest_by = 'timestamp'
	
	def __str__(self):
		"""
		Returns the model's string representation.
		"""
		return str(self.point) +': '+ str(self.team)


class AuthToken(models.Model):
	ROLES = (
		('LOG', _("Logbook Keeper")),
		('REG', _("Registrar"))
	)
	
	token = models.CharField(max_length=32, primary_key=True)
	role = models.CharField(max_length=3, choices=ROLES)
	race = models.ForeignKey(Race)
	point = models.ForeignKey(Point, null=True)
	expiration = models.PositiveIntegerField()
	
	def save(self, *args, **kwargs):
		"""
		Automatically add the token and expiration fields.
		"""
		while True:
			new_token = str(uuid.uuid4()).replace('-', '')
			try:
				AuthToken.objects.get(token=new_token)
			except AuthToken.DoesNotExist:
				break
		
		self.token = new_token
		self.expiration = int(time.time() + 24*60*60)
		
		super(AuthToken, self).save(*args, **kwargs)
	
	def __str__(self):
		"""
		Returns the model's string representation.
		"""
		return self.token

