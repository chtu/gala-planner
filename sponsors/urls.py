from django.conf.urls import url
from . import views

app_name = 'sponsors'

urlpatterns = [
	url(r'^all/(?P<gala_id>[0-9]+)/', views.all_sponsors, name="all_sponsors"),
	url(r'^(?P<invite_id>[0-9]+)/(?P<invite_code>\w+)/', views.create_sponsor, name='create_sponsor'),
	url(r'^details/(?P<gala_id>[0-9]+)/(?P<user_id>[0-9]+)/', views.sponsor_details, name='sponsor_details'),
	url(r'^invite-sent/(?P<gala_id>[0-9]+)/', views.invite_sent, name="invite_sent"),
	url(r'^resend-invite/(?P<gala_id>[0-9]+)/(?P<invite_id>[0-9]+)/', views.resend_invite, name="resend_invite"),
]