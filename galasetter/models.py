from django.db import models
from django.utils import timezone
import datetime


class Gala(models.Model):
	gala_name = models.CharField('event name', max_length=100, blank=False)
	gala_datetime = models.DateTimeField('event date', null=True)
	gala_num_tables = models.IntegerField('number of tables', default=0)
	gala_num_confirmed = models.IntegerField('number of confirmed guests', default=0)
	gala_num_invited = models.IntegerField('number of invited guests', default=0)
	gala_max_guests = models.IntegerField('maximum number of guests allowed', default=0)
	gala_has_limit = models.BooleanField('has maximum', default=False)
	date_created = models.DateTimeField('date created', auto_now_add=True, auto_now=False, null=True)
	date_updated = models.DateTimeField('date updated', auto_now_add=False, auto_now=True, null=True)

	def __str__(self):
		return self.gala_name

	def set_gala_datetime(self, year, month, day, hour, minute):
		try:
			t = timezone.now()

			if year >= t.year and year < 2099:
				self.gala_datetime = datetime.datetime(year, month, day, hour, minute, 0)
			else:
				raise ValueError("The year doesn't sound right!")
		except ValueError:
			raise ValueError("Some of the values are not valid")

	def gala_has_happened(self):
		if self.gala_datetime == None:
			return False

		d = timezone.now()
		current_datetime = datetime.datetime(d.year, d.month, d.day, d.hour, d.minute, 0)
		if self.gala_datetime < current_datetime:
			return True
		else:
			return False

class MealChoice(models.Model):
	gala = models.ForeignKey(Gala, on_delete=models.CASCADE)
	choice_text = models.CharField('meal choice', max_length=200)
	num_selected = models.IntegerField('number of times selected', default=0)


	def __str__(self):
		return self.choice_name