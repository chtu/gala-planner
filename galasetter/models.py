from django.db import models
from django.utils import timezone


class Gala(models.Model):
	gala_name = models.CharField('event name', max_length=100, blank=False)
	gala_datetime = models.DateTimeField('event date', blank=False)
	gala_num_tables = models.IntegerField('number of tables', default=0)
	gala_num_confirmed = models.IntegerField('number of confirmed guests', default=0)
	gala_num_invited = models.IntegerField('number of invited guests', default=0)
	gala_max_guests = models.IntegerField('maximum number of guests allowed', default=0)
	gala_has_limit = models.BooleanField('has maximum', default=False)
	date_created = models.DateTimeField('date created', auto_now_add=True, auto_now=False, null=True)
	date_updated = models.DateTimeField('date updated', auto_now_add=False, auto_now=True, null=True)

	def __str__(self):
		return gala_name

	def gala_has_happened(self):
		time = timezone.now()
		if time <= self.gala_datetime:
			return False
		else:
			return True

class MealChoice(models.Model):
	gala = models.ForeignKey(Gala, on_delete=models.CASCADE)
	choice_text = models.CharField('meal choice', max_length=200)
	num_selected = models.IntegerField('number of times selected', default=0)


	def __str__(self):
		return self.choice_name