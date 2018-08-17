from django.urls import path, include

from . import views

urlpatterns = [
	#path('<int:space_id>', include('reservationsApp.urls')),
	path('<int:space_id>/reservation/', include('reservationsApp.urls')),
]
