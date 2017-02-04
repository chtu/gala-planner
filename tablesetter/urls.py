from django.conf.urls import url
from . import views

app_name = "tablesetter"

urlpatterns = [
	url(r'^(?P<gala_id>[0-9]+)/allseats/', views.all_seats, name='all_seats'),
	url(r'^(?P<gala_id>[0-9]+)/alltables/', views.all_tables, name='all_tables'),
	url(r'^create/check/(?P<gala_id>[0-9]+)/', views.check_user, name="check_user"),
	url(r'^invite-sent/(?P<gala_id>[0-9]+)/', views.invite_sent, name="invite_sent"),
]