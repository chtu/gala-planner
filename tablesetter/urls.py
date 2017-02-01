from django.conf.urls import url
from . import views

app_name = "tablesetter"

urlpatterns = [
	url(r'^allseats', views.all_seats, name='all_seats'),
]