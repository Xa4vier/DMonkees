from django.shortcuts import render
from datetime import date
from rate_calculator import calculate
from django.http import HttpResponse
import rest_request
from trialLesson.forms import loginForm

# Create your views here.
def index(request):

	if request.method == 'POST':
		login_form = loginForm(request.POST)

		if login_form.is_valid():
			email =  login_form.cleaned_data['email']
			password = login_form.cleaned_data['password']

			context = {'email' : email, 'password' : password}
			return render(request, 'index.html', context = context)

	context = {'email' : 'test', 'password' : 'test'}
	return render(request, 'index.html', context = context)

def rateofpresence(request):
	context = calculate(rest_request.get_trialLessons(rest_request.get_token(), date(2017, 4, 2), date(2018, 7, 24)))

	return render(request, 'rateofpresence.html', context=context)

	