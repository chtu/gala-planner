from django.shortcuts import render

from .forms import PlannerSignupForm
from accounts.admin import UserCreationForm
from accounts.models import User


def planner_signup_form(request):
	form = UserCreationForm()
	context = {
		'form': form,
	}

	return render(request, "accounts/planner_signup_form.html", context)

def signed_up(request):
	form = UserCreationForm(request.POST)

	if form.is_valid():
		instance = form.save(commit=False)
		email = instance.email

		

		first_name = instance.first_name
		instance.save()

		context = {
			'first_name': first_name,
			'email': email,
		}

	context = {}

	return render(request, "accounts/signed_up.html", context)