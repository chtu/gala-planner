from django.shortcuts import render
from tablesetter.models import Gala

# Create your views here.
def all_seats(request):
	context = {}
	return render(request, 'tablesetter/seat_details.html', context)