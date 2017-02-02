from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from accounts.models import User
from tablesetter.models import Gala

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

def create_table(request, gala_id):
	context