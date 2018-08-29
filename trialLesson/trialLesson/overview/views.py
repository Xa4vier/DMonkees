from django.shortcuts import render
from datetime import date
from rate_calculator import calculate
import rest_request


# Create your views here.
def index(request):
	context = calculate(rest_request.get_trialLessons(rest_request.get_token(), date(2017, 4, 2), date(2018, 7, 24)))
	data = {'a': [[1, 2]] , 'b':  [[3, 4]] ,'c':[[5,6]]}
	
	return render(request, 'index.html', context=context)

	