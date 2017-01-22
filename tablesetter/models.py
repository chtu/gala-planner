from django.db import models
from accounts.models import User

# Create your models here.
class Table(models.Model):
	table_sponsor = models.ForeignKey(User, on_delete=models.CASCADE)
	table_size = models.IntegerField(blank=False)

	def __str__(self):
		return table_sponsor

class Guest(models.Model):
	table = models.ForeignKey(Table, on_delete=models.CASCADE)
	guest_first_name = models.CharField(max_length=50, blank=False)
	guest_last_name = models.CharField(max_length=50, blank=False)
	guest_email = models.EmailField(max_length = 50, blank=False)

	def __str__(self):
		return "%s %s" % (guest_first_name, guest_last_name)