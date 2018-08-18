from django.urls import path
from . import views

urlpatterns = [
	path('<int:reservation_id>', views.reservations_data, name='reservations_data'),
	path('delete/', views.delete, name='delete_reservation'),
	path('modify/', views.modify_reservations, name="modify_reservations"),
]
