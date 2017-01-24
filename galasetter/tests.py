import datetime

from django.test import TestCase
from .models import Gala, MealChoice
from django.utils import timezone

def create_gala(gala_name, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Gala.objects.create(gala_name=gala_name, gala_datetime=time)

class GalaMethodTests(TestCase):
	def test_current_date_is_after_gala_date(self):
		past_gala = create_gala("Test for a gala that has already happened.", -30)
		self.assertIs(past_gala.gala_has_happened(), True)

	def test_current_date_is_before_gala_date(self):
		future_gala = create_gala("Test for a gala that hasn't happened yet.", 30)
		self.assertIs(future_gala.gala_has_happened(), False)