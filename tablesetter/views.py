from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import UserCreationForm
from accounts.models import User
from errors import error_handler
from galasetter.models import Gala
from sponsors.forms import UserCheckForm
from sponsors.views import Invite
from tablesetter.forms import TableForm
from tablesetter.models import Table





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
				return HttpResponseRedirect(reverse('sponsors:invite_sent', args=(gala.id,)))
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









