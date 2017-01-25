import datetime

from django.test import TestCase
from .models import Gala, MealChoice
from django.utils import timezone


def _append_zero(integer):
	return str(integer).rjust(2, '0')

def _create_gala(gala_name, year, month, day, hour, minute):
	gala_year = str(year)
	gala_month = _append_zero(month)
	gala_day = _append_zero(day)
	gala_hour = _append_zero(hour)
	gala_minute = _append_zero(minute)
	gala_date = '%s-%s-%s' % (gala_year, gala_month, gala_day)
	gala_time = '%s:%s' % (gala_hour, gala_minute)
	return Gala.objects.create( gala_name=gala_name, gala_date=gala_date, gala_time=gala_time)

def create_gala(gala_name, days):
	d = timezone.now()
	d += datetime.timedelta(days=days)
	return _create_gala(gala_name, d.year, d.month, d.day, d.hour, d.minute)

class GalaMethodTests(TestCase):
	# Test for a past gala
	def test_current_date_is_after_gala_date(self):
		past_gala = create_gala("Test for a gala that has already happened.", -30)
		self.assertIs(past_gala.gala_has_happened(), True)
	# Test for a future gala
	def test_current_date_is_before_gala_date(self):
		future_gala = create_gala("Test for a gala that hasn't happened yet.", 30)
		self.assertIs(future_gala.gala_has_happened(), False)