import datetime

from django import forms
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from accounts.forms import UserCreationForm
from accounts.models import User, Invite
from galasetter.models import Gala
from tablesetter.models import Table



def planner_signup_form(request):
	form = UserCreationForm(request.POST or None)
	context = {
		'form': form,
	}

	if form.is_valid():
		instance = form.save(commit=False)

		first_name = instance.first_name
		instance.is_planner = True
		instance.save()

		context = {
			'first_name': first_name,
		}

	return render(request, "accounts/planner_signup_form.html", context)

def signed_up(request):
	context = {}

	return render(request, "accounts/signed_up.html", context)

def logout_view(request):
	logout(request)

	return HttpResponseRedirect(reverse('homepage:home'))

def create_sponsor(request, invite_id, invite_code):
	if not request.user.is_authenticated():
		try:
			invitation = Invite.objects.get(id=invite_id, code=invite_code, is_complete=False)
			gala = Gala.objects.get(id=invitation.gala_id)


			one_day_later = invitation.date_sent + datetime.timedelta(days=1)
			current_time = timezone.now()

			if one_day_later < current_time:
				invitation.delete()
				err_msg = "You waited too long so the invitation is no longer valid. Please contact your gala planner for another invitation."
				return render(request, 'homepage/error_page.html', {'err_msg': err_msg,})

			else:
				form = UserCreationForm(request.POST or None)

				if form.is_valid():
					form.save()
					invitation.is_complete = True
					invitation.save()

					for num in range(0, invitation.num_tables):
						Table.objects.create(sponsor_email=invitation.email, gala=gala)



					return HttpResponseRedirect(reverse('homepage:home'))
				else:
					form = UserCreationForm(initial={
							'email': invitation.email,
						})
					form.fields['email'].widget = forms.HiddenInput()
					context = {
						'form': form,
						'invitation': invitation,
					}
					return render(request, 'accounts/create_sponsor.html', context)

		except ObjectDoesNotExist:
			err_msg = "It's possible you are trying to access an invitation that is expired. Please contact your gala planner to receive another invitation."
			return render(request, 'homepage/error_page.html', {'err_msg': err_msg,})
	else:
		err_msg = "You're already logged in! If you're trying to create a new account, please log out and try again."
		return render(request, 'homepage/error_page.html', {'err_msg': err_msg,})