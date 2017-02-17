import datetime
from django.utils import timezone
from django.db import models




class Invite(models.Model):
	email = models.EmailField()
	is_complete = models.BooleanField(default=False)
	code = models.CharField(max_length=50, null=True)
	table_size = models.IntegerField(default=1)
	date_sent = models.DateTimeField(auto_now_add=True, auto_now=False)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		return email.lower()

	def is_expired(self):
		if not self.is_complete:
			invitation_period = 1

			current_dt = timezone.now()
			one_day_later = self.date_sent + datetime.timedelta(days=invitation_period)

			if one_day_later < current_dt:
				return True
			else:
				return False
		else:
			return False