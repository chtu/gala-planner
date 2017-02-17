import datetime

from django import forms
from django.contrib.auth import logout, login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from accounts.forms import UserCreationForm
from accounts.models import User
from errors import error_handler
from galasetter.models import Gala
from sponsors.models import Invite
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
