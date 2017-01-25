import datetime

from django.test import TestCase
from .models import Gala, MealChoice
from django.utils import timezone


def _create_gala(gala_name, year, month, day, hour, minute):
	gala_datetime = datetime.datetime(year, month, day, hour, minute, 0)
	return Gala.objects.create( gala_name=gala_name, gala_datetime=gala_datetime, )

def create_gala(gala_name, days):
	d = timezone.now()
	d += datetime.timedelta(days=days)
	return _create_gala(gala_name, d.year, d.month, d.day, d.hour, d.minute)

class GalaMethodTests(TestCase):
	#valid values
	t = timezone.now() + datetime.timedelta(days=30)
	y = t.year
	mo = t.month
	d = t.day
	h = t.hour
	mi = t.minute

	# Test for a past gala
	def test_current_date_is_after_gala_date(self):
		past_gala = create_gala("Test for a gala that has already happened.", -30)
		self.assertIs(past_gala.gala_has_happened(), True)
	# Test for a future gala
	def test_current_date_is_before_gala_date(self):
		future_gala = create_gala("Test for a gala that hasn't happened yet.", 30)
		self.assertIs(future_gala.gala_has_happened(), False)
	# Setting gala date with an invalid day
	def test_set_gala_datetime_with_invalid_day(self):
		invalid_gala = Gala.objects.create(gala_name="Gala with invalid day")
		invalid_day = 50
		with self.assertRaises(ValueError):
			invalid_gala.set_gala_datetime(self.y, self.mo, invalid_day, self.h, self.mi)
	# Setting the gala date with an invalid month
	def test_set_gala_datetime_with_invalid_month(self):
		invalid_gala = Gala.objects.create(gala_name="Gala with invalid month")
		invalid_month = 13
		with self.assertRaises(ValueError):
			invalid_gala.set_gala_datetime(self.y, invalid_month, self.d, self.h, self.mi)
	# Setting the gala date with an invalid year
	def test_set_gala_datetime_with_invalid_year(self):
		invalid_gala = Gala.objects.create(gala_name="Gala with invalid year")
		invalid_year = 2500
		with self.assertRaises(ValueError):
			invalid_gala.set_gala_datetime(invalid_year, self.mo, self.d, self.h, self.mi)

