
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from errors import error_handler

from accounts import invite_handler
from accounts.models import Invite, User
from galasetter.models import Gala
from tablesetter.models import Table


# HELPER FUNCTIONS
def get_tables_of_confirmed_users(gala):
	tables = Table.objects.all().exclude(user__isnull=True).filter(gala=gala)
	tables = tables.order_by('user__last_name', 'user__first_name', 'user__email')
	return tables

def get_confirmed_sponsors(gala):
	tables = get_tables_of_confirmed_users(gala)
	tables = tables.values('user__last_name', 'user__first_name', 'user__email').annotate(count=Count('user'))
	return tables

def get_pending_sponsors(gala):
	field = 'sponsor_email'
	tables = Table.objects.all().exclude(user__isnull=False).filter(gala=gala).order_by(field)
	tables = tables.values(field).annotate(count=Count(field))
	return tables

def get_pending_sponsors_with_expired_invitations(gala):
	invite_handler.delete_expired_invitations(gala)
	pending_sponsors = get_pending_sponsors(gala)
	users = []

	for sponsor in pending_sponsors:
		try:
			Invite.objects.get(email=sponsor['sponsor_email'])
		except ObjectDoesNotExist:
			users.append(sponsor)
	return users

def get_pending_sponsors_with_invitations(gala):
	invite_handler.delete_expired_invitations(gala)
	pending_sponsors = get_pending_sponsors(gala)
	users = []

	for sponsor in pending_sponsors:
		try:
			Invite.objects.get(email=sponsor['sponsor_email'])
			users.append(sponsor)
		except ObjectDoesNotExist:
			continue
	return users


# VIEWS
def all_sponsors(request, gala_id):
	if error_handler.is_auth_user(request):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			confirmed_sponsors = get_confirmed_sponsors(gala)
			pending_sponsors_with_inv = get_pending_sponsors_with_invitations(gala)
			pending_sponsors_without_inv = get_pending_sponsors_with_expired_invitations(gala)

			context = {
				'confirmed_sponsors': confirmed_sponsors,
				'gala': gala,
				'pending_sponsors_with_inv': pending_sponsors_with_inv,
				'pending_sponsors_without_inv': pending_sponsors_without_inv,
			}

			return render(request, 'sponsors/all_sponsors.html', context)
		except ObjectDoesNotExist:
			error_handler.unauth_err(request)
	else:
		error_handler.unauth_err(request)






















