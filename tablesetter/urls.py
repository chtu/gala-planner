from django.conf.urls import url
from . import views

app_name = "tablesetter"

urlpatterns = [
	url(r'^(?P<gala_id>[0-9]+)/allseats/', views.all_seats, name='all_seats'),
	url(r'^(?P<gala_id>[0-9]+)/alltables/', views.all_tables, name='all_tables'),
	url(r'^create/check/(?P<gala_id>[0-9]+)/', views.check_user, name="check_user"),
	url(r'^set-table-size/(?P<gala_id>[0-9]+)/', views.set_table_size, name="set_table_size"),
]