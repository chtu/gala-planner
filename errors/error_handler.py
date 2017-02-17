from django.contrib.auth import login
from django.shortcuts import render


def is_auth_planner(request):
	if request.user.is_authenticated() and request.user.is_planner:
		return True
	else:
		return False

def clear_sessions(request):
	if request.user.is_authenticated():
		user = request.user
		request.session.flush()
		login(request, user)
	else:
		request.session.flush()

def custom_err(request, err_msg):
	clear_sessions(request)
	context = {
		'err_msg': err_msg,
	}
	return render(request, 'errors/error_page.html', context)

def unauth_err(request):
	err_msg = "You are not authorized to view this page."
	return render(request, 'errors/error_page.html', {'err_msg': err_msg,})