from django.urls import path

from . import views

urlpatterns = [
    path('<int:space_id>/', views.space_data, name='space_data'),
    path('<int:space_id>/edit', views.space_data_admin, name='space_data_admin'),
    path('<int:space_id>/edit_fields', views.space_edit_fields, name='space_edit_fields'),
]
