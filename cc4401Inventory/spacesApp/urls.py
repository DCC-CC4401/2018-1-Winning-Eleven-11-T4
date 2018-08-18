from django.urls import path

from . import views

urlpatterns = [
    path('<int:space_id>/', views.space_data, name='space_data'),
]
