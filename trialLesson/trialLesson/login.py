from django.shortcuts import render

def authenticator(function, *args):
	def decorator(request, *args, **kwargs):
		if 'token' in request.session:
			return function(request)
		else :
			return render(request, 'index.html')
	return decorator