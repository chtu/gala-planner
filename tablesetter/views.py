from django.shortcuts import render
from tablesetter.models import Gala

# Create your views here.
def home(request):
	gala = Gala.objects.create(
		gala_name="My new gala",
		gala_date="1987-11-09",
		gala_time="5:50",
	)

	context = {
		'gala': gala,
	}

	return render(request, "tablesetter/home.html", context)