import random
import string

from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import UserCreationForm
from accounts.models import User, Invite
from errors import error_handler
from galasetter.models import Gala
from tablesetter.forms import InviteForm, TableForm, UserCheckForm
from tablesetter.models import Table


def generate_random_string():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase
		+ string.ascii_lowercase + string.digits) for _ in range(30))

def generate_invite_url(request, invitation):
	host = request.META['HTTP_HOST']
	url = "%s/accounts/%s/%s/" % (host, invitation.id, invitation.code)
	return url





def all_seats(request, gala_id):
	if (request.user.is_authenticated() and request.user.is_planner):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)
			context = {
				'gala': gala,
			}
			return render(request, 'tablesetter/all_seats.html', context)
		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)


def all_tables(request, gala_id):
	if (request.user.is_authenticated() and request.user.is_planner):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)
			tables = Table.objects.all().filter(gala=gala)

			field = 'sponsor_email'
			tables = tables.values(field).order_by(field).annotate(the_count=Count(field))

			context = {
				'gala': gala,
				'tables': tables,
			}
			return render(request, 'tablesetter/all_tables.html', context)

		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)


def check_user(request, gala_id):
	if request.user.is_authenticated() and request.user.is_planner:
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			# If the email was submitted
			form = UserCheckForm(request.POST or None)
			if form.is_valid():
				request.session['_user_check_post'] = request.POST
				return HttpResponseRedirect(reverse('tablesetter:set_table_size', args=(gala.id,)))
			else:
				context = {
					'gala': gala,
					'form': form,
				}
				return render(request, 'tablesetter/check_user.html', context)
		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)





def invite_sent(request, gala_id):
	if request.user.is_authenticated() and request.user.is_planner:
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			user_check_post = request.session.get('_user_check_post')
			table_post = request.session.get('_table_post')

			if (user_check_post is None) or (table_post is None):
				err_msg = "If you'd like to create a table for a sponsor, please start from the beginning."
				return error_handler.custom_err(request, err_msg)

			user_check_form = UserCheckForm(user_check_post)
			table_form = TableForm(table_post)

			# Form is guaranteed to be valid at this point
			if user_check_form.is_valid():
				email = user_check_form.cleaned_data.get('email')

			table_size = table_form.data.get('table_size')
			invites = Invite.objects.all().filter(email=email)

			if len(invites) == 0:
				invite_code = generate_random_string()
				invitation = Invite.objects.create(email=email, table_size=table_size, code=invite_code)

				url = generate_invite_url(request, invitation)

				context = {
					'email': email,
					'gala': gala,
					'url': url,
				}
			elif invites[0].is_complete:
				sponsor = User.objects.get(email=email)
				context = {
					'email': email,
					'gala': gala,
					'sponsor': sponsor,
				}
				error_handler.clear_sessions(request)
				Table.objects.create(sponsor_email=email, table_size=table_size, gala=gala, user=sponsor)
				return render(request, 'tablesetter/invite_sent.html', context)
			else:
				invitation = Invite.objects.get(email=email)
				url = generate_invite_url(request, invitation)
				context = {
					'email': email,
					'gala': gala,
					'invitation_pending': True,
					'url': url,
				}
			# Clear the session and create a new table
			error_handler.clear_sessions(request)
			Table.objects.create(sponsor_email=email, table_size=table_size, gala=gala)
			return render(request, 'tablesetter/invite_sent.html', context)

		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)



def set_table_size(request, gala_id):
	if request.user.is_authenticated() and request.user.is_planner:
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)
			user_check_post = request.session.get('_user_check_post')
			user_check_form = UserCheckForm(user_check_post)

			#I already know that the form is valid because it passthe validation tests
			if user_check_form.is_valid():
				email = user_check_form.cleaned_data.get('email')

			sponsor = User.objects.all().filter(email=email)

			table_form = TableForm(request.POST or None)

			if table_form.is_valid():
				request.session['_table_post'] = request.POST
				return HttpResponseRedirect(reverse('tablesetter:invite_sent', args=(gala.id,)))
			else:
				if len(sponsor) == 0:
					message = "It looks like a user does not exist yet."
					context = {
						'email': email,
						'gala': gala,
						'message': message,
						'table_form': table_form,
					}
				else:
					message = "A user already exists under the following information."
					context = {
						'gala': gala,
						'message': message,
						'sponsor': sponsor[0],
						'table_form': table_form,
					}
				return error_handler.render(request, 'tablesetter/set_table_size.html', context)

		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)











