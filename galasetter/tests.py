import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase

from .models import Gala, MealChoice
from .views import *


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
	# Test for a string representation of a normal date
	def test_str_representation_of_normal_date(self):
		gala = Gala.objects.create(
			gala_name="Gala with valid date",
			gala_date="2016-11-09", )
		self.assertEquals(gala.date_as_str(), "November 9, 2016")
	# Test of a gala with an invalid date
	def test_gala_with_an_invalid_date(self):
		gala_name = "Gala with invalid date"
		invalid_date = "2017-14-12"
		with self.assertRaises(ValidationError):
			Gala.objects.create(gala_name=gala_name, gala_date=invalid_date)
	# Test of a gala with an invalid time
	def test_gala_with_a_invalid_time(self):
		gala_name = "Gala with invalid time"
		invalid_time = "27:34"
		with self.assertRaises(ValidationError):
			Gala.objects.create(gala_name=gala_name, gala_date=invalid_time)
