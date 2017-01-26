from django.shortcuts import render
from accounts.forms import PlannerSignupForm


def landing(request):
	planner_signup_form = PlannerSignupForm()
	context = {
		'planner_signup_form': planner_signup_form,
	}

	return render(request, "landing/base.html", context)