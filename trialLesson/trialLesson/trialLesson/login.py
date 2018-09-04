def authenticator(func):
	def wrapper(request):
		return func()
	if 'token' in request.session:
		wrapper(request)