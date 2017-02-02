from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts.forms import UserCreationForm
from accounts.models import User
from galasetter.models import Gala
from tablesetter.forms import UserCheckForm
from tablesetter.models import Table

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
	if (request.user.is_authenticated() and request.user.is_planner):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			# If the email was submitted
			if request.POST:
				form = UserCheckForm(request.POST)

				# User with the email already exists
				try:
					email = form.cleaned_data.get('email')
					sponsor = User.objects.get(email=email, is_planner=True)

					form = UserCheckForm()

					context = {
						'form': form,
						'gala': gala,
						'email': email,
						'sponsor': sponsor,
					}
				# User with email does not exist
				except ObjectDoesNotExist:
					email = form.cleaned_data.get('email')
					creation_form = UserCreationForm(initial={
							'email': email,
							'password1': 'finntinycoco',
							'password2': 'finntinycoco',
						})
					context = {
						'creation_form': creation_form,
						'email': email,
						'gala': gala,
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





