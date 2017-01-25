from django.db import models
from django.utils import timezone
import datetime

class Gala(models.Model):
	gala_name = models.CharField('event name', max_length=100, blank=False)
	gala_date = models.DateField('event date', null=True)
	gala_time = models.TimeField('event time', null=True)
	gala_num_tables = models.IntegerField('number of tables', default=0)
	gala_num_confirmed = models.IntegerField('number of confirmed guests', default=0)
	gala_num_invited = models.IntegerField('number of invited guests', default=0)
	gala_max_guests = models.IntegerField('maximum number of guests allowed', default=0)
	gala_has_limit = models.BooleanField('has maximum', default=False)
	date_created = models.DateTimeField('date created', auto_now_add=True, auto_now=False, null=True)
	date_updated = models.DateTimeField('date updated', auto_now_add=False, auto_now=True, null=True)

	def __str__(self):
		return self.gala_name

	def gala_has_happened(self):
		if self.gala_date == None or self.gala_time == None:
			return False

		d = timezone.now()
		current_datetime = datetime.datetime(d.year, d.month, d.day, d.hour, d.minute, 0)

		year, month, day = self.gala_date.split("-")
		hour, minute = self.gala_time.split(":")

		gala_datetime = datetime.datetime(
			int(year),
			int(month),
			int(day),
			int(hour),
			int(minute),
			0
		)

		if gala_datetime < current_datetime:
			return True
		else:
			return False

	def date_as_str(self):
		months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
			'October', 'November', 'December']
		year, month, day = self.gala_date.split("-")
		str_month = months_list[int(month)-1]

		return "%s %s, %s" % (str_month, int(day), year)


class MealChoice(models.Model):
	gala = models.ForeignKey(Gala, on_delete=models.CASCADE)
	choice_text = models.CharField('meal choice', max_length=200)
	num_selected = models.IntegerField('number of times selected', default=0)


	def __str__(self):
		return self.choice_name