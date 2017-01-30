from django.conf.urls import url

from . import views

app_name = 'galasetter'

urlpatterns = [
	url(r'^$', views.gala_index, name="gala_index"),
	url(r'^create/', views.create, name="create"),
	url(r'^update/(?P<gala_id>[0-9]+)/$', views.update, name="update"),
]