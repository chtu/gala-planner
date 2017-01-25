from django.shortcuts import render
from tablesetter.models import Gala

# Create your views here.
def home(request):
	gala = Gala.objects.create(
		gala_name="My new gala",
	)

	gala.set_gala_datetime(2016, 11, 9, 8, 23)

	context = {
		'gala': gala,
	}

	return render(request, "tablesetter/home.html", context)