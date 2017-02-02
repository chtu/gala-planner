from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import UserCreationForm
from accounts.models import User, Invite
from tablesetter.models import Table

def create_sponsor(request, invite_sent, invite_id):
	try:
		invite = Invite.objects.get()


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
	form = UserCreationForm(request.POST)

	if form.is_valid():
		instance = form.save(commit=False)

		first_name = instance.first_name
		instance.save()

		context = {
			'first_name': first_name,
		}

	context = {}

	return render(request, "accounts/signed_up.html", context)

def logout_view(request):
	logout(request)

	return HttpResponseRedirect(reverse('homepage:home'))

def create_sponsor(request):
	