from django.conf.urls import url
from . import views

app_name = "landing"

urlpatterns = [
	url(r'^$', views.landing, name='landing'),
]