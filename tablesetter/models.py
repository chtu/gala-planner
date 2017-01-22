from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator

# Create your models here.

'''
class Gala(models.Model):
	gala_name = models.CharField(max_length=100)
	gala_date = models.DateTimeField('event date')
	gala_num_tables = models.IntegerField()
	gala_total_guests = models.IntegerField()

	def __str__(self):
		return gala_name

class Table(models.Model):
	gala = models.ForeignKey(Gala, on_delete=models.CASCADE)
	table_sponsor = models.ForeignKey(User, on_delete=models.CASCADE)
	table_size = models.IntegerField(blank=False, validators=[MaxValueValidator(100)])

	def __str__(self):
		return table_sponsor

class Guest(models.Model):
	table = models.ForeignKey(Table, on_delete=models.CASCADE)
	guest_first_name = models.CharField(max_length=50, blank=False, null=True)
	guest_last_name = models.CharField(max_length=50, blank=False, null=True)
	guest_email = models.EmailField(max_length = 200, blank=False, null=True)
	has_replied = models.BooleanField(default=False)
	dietary_restrictions = models.CharField(max_length=300, blank=True, null=True)

	def __str__(self):
		return "%s %s" % (guest_first_name, guest_last_name)
		'''