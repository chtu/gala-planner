import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import GalaForm, GalaUpdateForm
from .models import Gala, MealChoice


def gala_index(request):
	try:
		galas = Gala.objects.all().filter(gala_date__gte=datetime.date.today()).filter(user_id=request.user)
		galas = galas.order_by('gala_date', 'gala_time')

		context = {
			'galas': galas,
		}

	except ObjectDoesNotExist:
		print("Uh oh! You got an error!")
		context = {}

	return render(request, 'galasetter/gala_list.html', context)

def update(request, gala_id):
	try:
		gala = Gala.objects.get(id=gala_id, user_id=request.user)

		form = GalaUpdateForm(request.POST or None)

		if form.is_valid():
			name = form.cleaned_data.get('gala_name')
			date = form.cleaned_data.get('gala_date')
			time = form.cleaned_data.get('gala_time')

			if name != "":
				gala.gala_name = name
			if date != None:
				gala.gala_date = date
			if time != None:
				gala.gala_time = time

			gala.save()

			return HttpResponseRedirect(reverse('galasetter:gala_index'))

		context = {
			'gala': gala,
			'form': form,
		}

		return render(request, 'galasetter/gala_update.html', context)
	except ObjectDoesNotExist:
		error_message = "Uh oh! It looks like you took a wrong turn!"
		context = {
			'error_message': error_message,
		}
		return render(request, 'homepage/error_page.html', context)

def create(request):
	form = GalaForm(request.POST or None)

	if form.is_valid():
		name = form.cleaned_data.get('gala_name')
		date = form.cleaned_data.get('gala_date')
		time = form.cleaned_data.get('gala_time')

		Gala.objects.create(gala_name=name, gala_date=date, gala_time=time, user_id=request.user)

		return HttpResponseRedirect(reverse('galasetter:gala_index'))

	context = {
		'form': form,
	}

	return render(request, 'galasetter/gala_create.html', context)