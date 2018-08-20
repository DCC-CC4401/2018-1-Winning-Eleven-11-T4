from django.urls import path
from . import views

urlpatterns = [
    path('<int:reservation_id>', views.reservations_data, name='reservations_data'),
    path('<int:reservation_id>/cancel_reservation', views.user_cancel_reservation, name='user_cancel_reservation'),
    path('delete/', views.delete, name='delete_reservation'),
    path('modify/', views.modify_reservations, name="modify_reservations"),
]
