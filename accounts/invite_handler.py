import datetime
from django.utils import timezone

from .models import Invite
from tablesetter.models import Table


def delete_expired_invitations(gala):
	invites = Invite.objects.all().filter(is_complete=False)

	for invite in invites:
		if invite.is_expired():
			invite.delete()