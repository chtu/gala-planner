from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import UserCreationForm, UserSigninForm


def home(request):
	if request.user.is_authenticated():
		last_name = request.user.last_name

		context = {
			'last_name': last_name,
		}
	else:
		form = UserSigninForm(request.POST or None)
		message = "Sign into your account:"

		context = {
			'form': form,
			'message': message,
		}

		if request.POST:
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(username=email, password=password)

			if user is not None:
				login(request, user)
			else:
				message = "The email/password combination was incorrect."
				context = {
					'form': form,
					'message': message,
				}

	return render(request, 'homepage/base.html', context)