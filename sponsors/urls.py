from django.conf.urls import url
from . import views

app_name = 'sponsors'

urlpatterns = [
	url(r'^all/(?P<gala_id>[0-9]+)/', views.all_sponsors, name="all_sponsors"),
]