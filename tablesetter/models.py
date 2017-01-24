from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator


class Gala(models.Model):
	gala_name = models.CharField('event name', max_length=100, blank=False)
	gala_datetime = models.DateTimeField('event date', blank=False)
	gala_num_tables = models.IntegerField('number of tables',)
	gala_total_guests = models.IntegerField('maximum number of guests',)
	date_created = models.DateTimeField('date created', auto_now_add=True, auto_now=False, null=True)
	date_updated = models.DateTimeField('date updated', auto_now_add=False, auto_now=True, null=True)

	def __str__(self):
		return gala_name

class MealChoice(models.Model):
	gala = models.ForeignKey(Gala, on_delete=models.CASCADE)
	choice_name = models.CharField('meal choice', max_length=200)

	def __str__(self):
		return self.choice_name

#In this class, our 'user' is basically a table sponsor who buys the table at the gala
class Table(models.Model):
	gala = models.ForeignKey(Gala, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	table_sponsor_name = models.CharField('table sponsor', max_length=150, blank=False)
	table_size = models.IntegerField(blank=False, validators=[MaxValueValidator(99)])
	date_created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	date_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

	def __str__(self):
		return table_sponsor

class Party(models.Model):
	table = models.ForeignKey(Table, on_delete=models.CASCADE)
	party_contact = models.CharField('full name of party contact', max_length=150)

	def __str__(self):
		return self.party_contact

class Seat(models.Model):
	table = models.ForeignKey(Table, on_delete=models.CASCADE)
	party = models.ForeignKey(Party, on_delete=models.CASCADE, null=True)
	details_completed = models.BooleanField(default=False)
	is_donated = models.BooleanField(default=False)
	seat_number = models.IntegerField('seat number')

class SeatDetails(models.Model):
	seat = models.OneToOneField(Seat)
	guest_first_name = models.CharField(max_length=50, blank=False)
	guest_last_name = models.CharField(max_length=50, blank=False)
	meal_choice = models.CharField('meal choice', max_length=200, blank=False)
	dietary_restrictions = models.CharField('dietary restrictions', max_length=300, blank=True)
	special_accommodations = models.CharField(max_length=300, blank=True)
	initial_response_date = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	date_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
