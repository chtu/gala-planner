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

		context = {
			'form': form,
		}

		if request.POST:
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(username=email, password=password)

			if user is not None:
				login(request, user)

	return render(request, 'homepage/base.html', context)