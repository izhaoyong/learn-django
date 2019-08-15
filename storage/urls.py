from django.urls import path

from . import views


urlpatterns = [
	# ex: /storage/
	path('', views.index, name='index')
]
