from django.conf.urls import url
from . import views


app_name = "accounts"

urlpatterns = [
	url(r'^$', views.planner_signup_form, name="planner_signup_form"),
	url(r'^create/(?P<invite_sent>[0-9]+)/(?P<invite_id>[0-9]+)/', views.create_sponsor, name="create_sponsor"),
	url(r'^logout/', views.logout_view, name="logout"),
	url(r'^signedup/', views.signed_up, name="signed_up"),
]