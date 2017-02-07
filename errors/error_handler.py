from django.contrib.auth import login
from django.shortcuts import render


def is_auth_user(request):
	if request.user.is_authenticated() and request.user.is_planner:
		return True
	else:
		return False

def clear_sessions(request):
	user = request.user
	request.session.flush()
	login(request, user)

def custom_err(request, err_msg):
	clear_sessions(request)
	context = {
		'err_msg': err_msg,
	}
	return render(request, 'homepage/error_page.html', context)

def unauth_err(request):
	err_msg = "You are unauthorized to view this page."
	return render(request, 'homepage/error_page.html', {'err_msg': err_msg,})