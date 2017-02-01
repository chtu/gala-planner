from django.db import models
from django.core.validators import MaxValueValidator

from accounts.models import User
from galasetter.models import Gala, MealChoice


class Table(models.Model):
	gala = models.ForeignKey(Gala, on_delete=models.CASCADE)
	table_sponsor = models.ForeignKey(User, null=True)
	table_size = models.IntegerField(blank=False, validators=[MaxValueValidator(99)])
	date_created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	date_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	def __str__(self):
		return self.table_sponsor


class Seat(models.Model):
	table = models.ForeignKey(Table, on_delete=models.CASCADE)
	invite_is_pending = models.BooleanField(default=False)
	last_invite_sent = models.DateTimeField(null=True)
	details_completed = models.BooleanField(default=True)
	is_donated = models.BooleanField(default=False)


class SeatDetails(models.Model):
	seat = models.OneToOneField(Seat)
	guest_first_name = models.CharField("guest's first name", max_length=50, blank=False)
	guest_last_name = models.CharField("guest's last name", max_length=50, blank=False)
	meal_choice = models.CharField('meal choice', max_length=300, blank=False)
	dietary_restrictions = models.CharField('dietary restrictions', max_length=300, blank=True)
	special_accommodations = models.CharField("special accommodations", max_length=300, blank=True)
	initial_response_date = models.DateTimeField("initial response date", auto_now_add=True, auto_now=False, null=True)
	date_updated = models.DateTimeField("date updated", auto_now_add=False, auto_now=True, null=True)





