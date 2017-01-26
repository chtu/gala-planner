from django.conf.urls import url
from . import views


app_name = "accounts"

urlpatterns = [
	url(r'^planner', views.planner_signup_form, name="planner_signup_form"),
	url(r'^signedup', views.signed_up, name="signed_up"),
]