from django.shortcuts import render
from datetime import date
from rate_calculator import calculate
from django.http import HttpResponse
from rest_request import get_token, get_trialLessons
from trialLesson.forms import loginForm
from login import authenticator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect, redirect
import time



# Create your views here.
def index(request):

	# check if request is post
	if request.method == 'POST':
		login_form = loginForm(request.POST) #bind to form
		time.sleep(1)

		if login_form.is_valid(): 
			username =  login_form.cleaned_data['username'] # get username
			password = login_form.cleaned_data['password'] # get password

			token = get_token(username, password) # get token
			if 'error' in token:
				 return render(request, 'index.html', {'message' : 'error with logging in'})
			else :
				user = authenticate(request, username=username, password=password)
				login(request, user)
				request.session['token'] = token['access_token']
				return render(request, 'rateofpresence.html')
		else:
			return render(request, 'index.html')


	else : # first time the page is requested
		return render(request, 'index.html')

@authenticator
def rateofpresence(request):
	
	context = calculate(get_trialLessons(request.session['token'], date(2017, 4, 2), date(2018, 7, 24)))
	context['token'] = request.session['token']
	return render(request, 'rateofpresence.html', context=context)

def logoutv(request):
	logout(request)
	return redirect('/')
	return HttpResponseRedirect('/overview/')
	