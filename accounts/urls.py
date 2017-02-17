from django.conf.urls import url
from . import views


app_name = "accounts"

urlpatterns = [
	url(r'^$', views.planner_signup_form, name="planner_signup_form"),
	url(r'^logout/', views.logout_view, name="logout"),
	url(r'^signedup/', views.signed_up, name="signed_up"),
]