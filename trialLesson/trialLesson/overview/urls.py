from django.urls import path
from overview import views


urlpatterns = [
	path('', views.index, name='index'),
	path('rateofpresence', views.rateofpresence, name='rateofpresence')
]