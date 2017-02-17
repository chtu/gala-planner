
import datetime
import random
import string

from django import forms
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from errors import error_handler

from sponsors import invite_handler
from accounts.forms import UserCreationForm
from accounts.models import User
from galasetter.models import Gala
from sponsors.forms import UserCheckForm
from sponsors.models import Invite
from tablesetter.forms import TableForm
from tablesetter.models import Seat, Table


# HELPER FUNCTIONS
def get_tables_of_confirmed_users(gala):
	tables = Table.objects.all().exclude(user__isnull=True).filter(gala=gala)
	tables = tables.order_by('user__last_name', 'user__first_name', 'user__email')
	return tables

def get_confirmed_sponsors(gala):
	tables = get_tables_of_confirmed_users(gala)
	tables = tables.values('user__last_name', 'user__first_name', 'user__email', 'user__id').annotate(count=Count('user'))
	return tables

def get_pending_sponsors(gala):
	field = 'sponsor_email'
	tables = Table.objects.all().exclude(user__isnull=False).filter(gala=gala).order_by(field)
	tables = tables.values(field).annotate(count=Count(field))
	return tables

def get_pending_sponsors_with_expired_invitations(gala):
	pending_sponsors = get_pending_sponsors(gala)
	users = []
	for sponsor in pending_sponsors:
		try:
			invite = Invite.objects.get(email=sponsor['sponsor_email'], is_complete=False)
			if invite.is_expired():
				sponsor['invite_id'] = invite.id
				users.append(sponsor)
		except ObjectDoesNotExist:
			continue
	return users

def get_pending_sponsors_with_invitations(gala):
	pending_sponsors = get_pending_sponsors(gala)
	users = []

	for sponsor in pending_sponsors:
		try:
			invite = Invite.objects.get(email=sponsor['sponsor_email'], is_complete=False)
			if not invite.is_expired():
				users.append(sponsor)
		except ObjectDoesNotExist:
			continue
	return users


# VIEWS
def all_sponsors(request, gala_id):
	if error_handler.is_auth_planner(request):
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
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)



def get_seats_lists(tables):
	seats_list = {}
	for table in tables:
		seats = Seat.objects.all().filter(table=table)
		key = "%i" % (table.id)
		seats_list[key] = seats
	return seats_list

def sponsor_details(request, gala_id, user_id):
	if error_handler.is_auth_planner(request):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)
			sponsor = User.objects.get(id=user_id)
			tables = Table.objects.all().filter(user=sponsor, gala=gala)
			seats_list = get_seats_lists(tables)

			context = {
				'gala': gala,
				'seats_list': seats_list,
				'sponsor': sponsor,
				'tables': tables,
			}

			return render(request, 'sponsors/sponsor_details.html', context)
		except:
			print("Error happened while getting objects.")
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)






# Helper functions for invite_sent()
def generate_invite_url(request, invitation):
	host = request.META['HTTP_HOST']
	url = "%s/sponsors/%s/%s/" % (host, invitation.id, invitation.code)
	return url

def generate_random_string():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase
		+ string.ascii_lowercase + string.digits) for _ in range(30))

def set_table_and_send_invite(request, email, table_size, gala):
	try:
		invite = Invite.objects.get(email=email)

		if invite.is_complete:
			sponsor = User.objects.get(email=email)
			context = {
				'email': email,
				'gala': gala,
				'sponsor': sponsor,
			}
			Table.objects.create(sponsor_email=email, table_size=table_size, gala=gala, user=sponsor)
			error_handler.clear_sessions(request)
			return render(request, 'sponsors/invite_sent.html', context)
		else:
			if invite.is_expired():
				current_dt = timezone.now()
				invite.date_sent = current_dt
				invite.code = generate_random_string()
				invite.save()

				url = generate_invite_url(request, invite)
				context = {
					'email': email,
					'gala': gala,
					'invitation_pending': True,
					'invitation_expired': True,
					'url': url,
				}
			else:
				url = generate_invite_url(request, invite)
				context = {
					'email': email,
					'gala': gala,
					'invitation_pending': True,
					'url': url,
				}
			error_handler.clear_sessions(request)
			Table.objects.create(sponsor_email=email, table_size=table_size, gala=gala)
			return render(request, 'sponsors/invite_sent.html', context)
	except ObjectDoesNotExist:
		# Code to create a brand new invitation
		invite_code = generate_random_string()
		invitation = Invite.objects.create(email=email, table_size=table_size, code=invite_code)
		url = generate_invite_url(request, invitation)

		context = {
			'email': email,
			'gala': gala,
			'url': url,
		}
		Table.objects.create(sponsor_email=email, table_size=table_size, gala=gala)
		error_handler.clear_sessions(request)
		return render(request, 'sponsors/invite_sent.html', context)

# View
def invite_sent(request, gala_id):
	if error_handler.is_auth_planner(request):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			user_check_post = request.session.get('_user_check_post')
			table_post = request.session.get('_table_post')

			if (user_check_post is None) or (table_post is None):
				err_msg = "If you'd like to create a table for a sponsor, please start from the beginning."
				return error_handler.custom_err(request, err_msg)

			user_check_form = UserCheckForm(user_check_post)
			table_form = TableForm(table_post)
			# The following post data is guaranteed to be valid, so I can get the raw data
			email = user_check_form.data.get('email')
			table_size = table_form.data.get('table_size')

			return set_table_and_send_invite(request, email, table_size, gala)
			
		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)






def initialize_table_seats(table):
	for num in range(0, table.table_size):
		Seat.objects.create(table=table)

# View to create new sponsors
def create_sponsor(request, invite_id, invite_code):
	if request.user.is_authenticated() == False:
		try:
			invitation = Invite.objects.get(id=invite_id, code=invite_code)

			if invitation.is_complete == True:
				err_msg = "You already created an account with us! Simply go to the home page and sign in."
				return error_handler.custom_err(request, err_msg)
			else:
				if invitation.is_expired():
					err_msg = "You waited too long so the invitation is no longer valid. Please contact your gala planner for another invitation."
					return error_handler.custom_err(request, err_msg)

				else:
					form = UserCreationForm(request.POST or None)

					if form.is_valid():
						email = form.cleaned_data.get('email')
						form.save()
						invitation.is_complete = True
						invitation.save()
						user = User.objects.get(email=email)


						all_tables = Table.objects.all().filter(sponsor_email=email)

						if len(all_tables) != 0:
							for table in all_tables:
								table.user = user
								table.save()

						for table in all_tables:
							initialize_table_seats(table);

						login(request, user)

						return HttpResponseRedirect(reverse('homepage:home'))
					else:
						if request.POST:
							message = "An error occurred! Please make sure you type your password correctly in both boxes and include all necessary fields."
						else:
							message = "Please fill out the following information to create your account."

						form = UserCreationForm(initial={
								'email': invitation.email,
							})
						form.fields['email'].widget = forms.HiddenInput()
						context = {
							'form': form,
							'invitation': invitation,
							'message': message,
						}
						return render(request, 'accounts/create_sponsor.html', context)

		except ObjectDoesNotExist:
			err_msg = "It's possible you are trying to access an invitation that is expired. Please contact your gala planner to receive another invitation."
			return error_handler.custom_err(request, err_msg)
	else:
		err_msg = "You're already logged in! If you're trying to create a new account, please log out and try again."
		return error_handler.custom_err(request, err_msg)



def resend_invite(request, gala_id, invite_id):
	if error_handler.is_auth_planner(request):
		gala = Gala.objects.get(id=gala_id, user_id=request.user)
		invite = Invite.objects.get(id=invite_id)

		invite.date_sent = timezone.now()
		invite.code = generate_random_string()
		invite.save()

		url = generate_invite_url(request, invite)

		context = {
			'gala': gala,
			'invite': invite,
			'url': url,
		}

		return render(request, 'sponsors/invite_resent.html', context)

	else:
		return error_handler.unauth_err(request)


