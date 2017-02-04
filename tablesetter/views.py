import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts.forms import UserCreationForm
from accounts.models import User, Invite
from galasetter.models import Gala
from tablesetter.forms import InviteForm, UserCheckForm
from tablesetter.models import Table


def generate_random_string():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase
		+ string.ascii_lowercase + string.digits) for _ in range(30))

# Create your views here.
def all_seats(request, gala_id):
	if (request.user.is_authenticated() and request.user.is_planner):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)
			context = {
				'gala': gala,
			}
			return render(request, 'tablesetter/all_seats.html', context)
		except ObjectDoesNotExist:
			return render(request, 'homepage/error_page.html', {})
	else:
		return render(request, 'homepage/error_page.html', {})

def all_tables(request, gala_id):
	if (request.user.is_authenticated() and request.user.is_planner):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			context = {
				'gala': gala,
			}
			return render(request, 'tablesetter/all_tables.html', context)
		except ObjectDoesNotExist:
			return render(request, 'homepage/error_page.html', {})
	else:
		return render(request, 'homepage/error_page.html', {})

def check_user(request, gala_id):
	if request.user.is_authenticated() and request.user.is_planner:
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			# If the email was submitted
			if request.POST:
				form = UserCheckForm(request.POST)
				if form.is_valid():
					email = form.cleaned_data.get('email')
					# User with the email already exists
					try:
						sponsor = User.objects.get(email=email, is_planner=False)

						form = UserCheckForm()
						user_found = True

						context = {
							'form': form,
							'gala': gala,
							'email': email,
							'sponsor': sponsor,
							'user_found': user_found,
						}
					# User with email does not exist
					except ObjectDoesNotExist:
						form = UserCheckForm()
						num_tables = 1
						user_not_found = True
						invite_form = InviteForm(initial={
								'email': email,
								'num_tables': num_tables,
							})

						context = {
							'email': email,
							'form': form,
							'gala': gala,
							'invite_form': invite_form,
							'user_not_found': user_not_found,
						}
					return render(request, 'tablesetter/check_user.html', context)
				else:
					form = UserCheckForm()

					context = {
						'gala': gala,
						'form': form,
					}
					return render(request, 'tablesetter/check_user.html', context)
			# Email not submitted yet
			else:
				form = UserCheckForm()

				context = {
					'gala': gala,
					'form': form,
				}
				return render(request, 'tablesetter/check_user.html', context)
		except ObjectDoesNotExist:
			return render(request, 'homepage/error_page.html', {})
	else:
		return render(request, 'homepage/error_page.html', {})



def invite_sent(request, gala_id):
	if request.user.is_authenticated() and request.user.is_planner and request.POST:
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			invite_form = InviteForm(request.POST)
			email = invite_form.data.get('email')

			try:
				invitation = Invite.objects.get(email=email)

				if invitation.is_complete:
					err_msg = "This user already created an account."
				else:
					err_msg = "An invitation was already sent to this user."
				return render(request, 'homepage/error_page.html', {'err_msg': err_msg,})

			except ObjectDoesNotExist:
				if invite_form.is_valid():
					invite_form_is_valid = True
					num_tables = invite_form.cleaned_data.get('num_tables')

					invite_code = generate_random_string()

					invitation = Invite.objects.create(email=email, code=invite_code, num_tables=num_tables, gala_id=gala.id)

					#For testing purposes
					host = request.META['HTTP_HOST']

					url = "%s/accounts/%s/%s/" % (host, invitation.id, invite_code)

					context = {
						'email': email,
						'gala': gala,
						'invite_form_is_valid': invite_form_is_valid,
						'url': url,
					}
				return render(request, 'tablesetter/invite_sent.html', context)
		except ObjectDoesNotExist:
			return render(request, 'homepage/error_page.html', {})
	else:
		return render(request, 'homepage/error_page.html', {})


