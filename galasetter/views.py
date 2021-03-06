import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import AddMealChoiceForm, EditMealChoiceForm, GalaForm, GalaUpdateForm
from .models import Gala, MealChoice
from errors import error_handler
from tablesetter.models import Table



def gala_list(request):
	if error_handler.is_auth_planner(request):
		future_galas = Gala.objects.all().filter(gala_date__gte=datetime.date.today()).filter(user_id=request.user)
		future_galas = future_galas.order_by('gala_date', 'gala_time')
		future_gala_message = "You have %i upcoming galas." % (len(future_galas))

		context = {
			'future_galas': future_galas,
			'future_gala_message': future_gala_message,
		}

		return render(request, 'galasetter/gala_list.html', context)
	else:
		return error_handler.unauth_err(request)


def update(request, gala_id):
	if error_handler.is_auth_planner(request):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			if request.POST:
				form = GalaUpdateForm(request.POST)
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

					return HttpResponseRedirect(reverse('galasetter:details', args=(gala.id,)))
			else:
				form = GalaUpdateForm(initial={
						'gala_name': gala.gala_name,
						'gala_date': gala.gala_date,
						'gala_time': gala.gala_time,
					})

			context = {
				'gala': gala,
				'form': form,
			}

			return render(request, 'galasetter/gala_update.html', context)
		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)


def create(request):
	if error_handler.is_auth_planner(request):
		form = GalaForm(request.POST or None)

		if form.is_valid():
			name = form.cleaned_data.get('gala_name')
			date = form.cleaned_data.get('gala_date')
			time = form.cleaned_data.get('gala_time')

			Gala.objects.create(gala_name=name, gala_date=date, gala_time=time, user_id=request.user)

			return HttpResponseRedirect(reverse('galasetter:gala_list'))
		else:
			context = {
				'form': form,
			}
			return render(request, 'galasetter/gala_create.html', context)
	else:
		return error_handler.unauth_err(request)


def details(request, gala_id):
	if error_handler.is_auth_planner(request):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			meal_choices = MealChoice.objects.all().filter(gala=gala)

			meal_choice_message = "You have %i meal choices set." % (len(meal_choices))

			context = {
				'gala': gala,
				'meal_choice_message': meal_choice_message,
				'meal_choices': meal_choices,
			}

			return render(request, 'galasetter/gala_details.html', context)
		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)


def add_meal_choice(request, gala_id):
	if error_handler.is_auth_planner(request):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)

			form = AddMealChoiceForm(request.POST or None)

			context = {
				'gala': gala,
				'form': form,
			}

			if form.is_valid():
				instance = form.save(commit=False)

				MealChoice.objects.create(
					gala=gala,
					choice_text=instance.choice_text,
					choice_desc=instance.choice_desc
				)

				return HttpResponseRedirect(reverse('galasetter:details', args=(gala.id,)))

			return render(request, 'galasetter/add_meal_choice.html', context)
		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)


def edit_meal_choice(request, gala_id, mealchoice_id):
	if error_handler.is_auth_planner(request):
		try:
			gala = Gala.objects.get(id=gala_id, user_id=request.user)
			mealchoice = MealChoice.objects.get(id=mealchoice_id, gala=gala)

			if request.POST:
				form = EditMealChoiceForm(request.POST)

				if form.is_valid():
					text = form.cleaned_data.get('choice_text')
					desc = form.cleaned_data.get('choice_desc')

					if text != "":
						mealchoice.choice_text = text
					if desc != "":
						mealchoice.choice_desc = desc
					mealchoice.save()

					return HttpResponseRedirect( reverse('galasetter:details', args=(gala.id,) ))
			else:
				form = EditMealChoiceForm(initial={
						'choice_text': mealchoice.choice_text,
						'choice_desc': mealchoice.choice_desc,
					})
			context = {
				'gala': gala,
				'mealchoice': mealchoice,
				'form': form,
			}

			return render(request, 'galasetter/edit_meal_choice.html', context)
		except ObjectDoesNotExist:
			return error_handler.unauth_err(request)
	else:
		return error_handler.unauth_err(request)









