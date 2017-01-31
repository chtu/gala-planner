from django.conf.urls import url

from . import views

app_name = 'galasetter'

urlpatterns = [
	url(r'^$', views.gala_list, name="gala_list"),
	url(r'^addmealchoice/(?P<gala_id>[0-9]+)/$', views.add_meal_choice, name="add_meal_choice"),
	url(r'^create/', views.create, name="create"),
	url(r'^details/(?P<gala_id>[0-9]+)/$', views.details, name="details"),
	url(r'^editmealchoice/(?P<gala_id>[0-9]+)/(?P<mealchoice_id>[0-9]+)/$', views.edit_meal_choice, name="edit_meal_choice"),
	url(r'^update/(?P<gala_id>[0-9]+)/$', views.update, name="update"),
]