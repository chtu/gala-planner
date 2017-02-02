from django.conf.urls import url
from . import views

app_name = "tablesetter"

urlpatterns = [
	url(r'^(?P<gala_id>[0-9]+)/allseats', views.all_seats, name='all_seats'),
	url(r'^(?P<gala_id>[0-9]+)/alltables', views.all_tables, name='all_tables'),
	url(r'^(?P<gala_id>[0-9]+)/createtable', views.create_table, name="create_table"),
]