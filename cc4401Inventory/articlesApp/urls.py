from django.urls import path

from . import views

urlpatterns = [
    path('<int:article_id>/', views.article_data, name='article_data'),
    path('<int:article_id>/edit', views.article_data_admin, name='article_data_admin'),
    path('<int:article_id>/delete', views.delete_item, name='delete_item'),
    path('<int:article_id>/edit_fields', views.article_edit_fields, name='article_edit_fields'),
    path('request', views.article_request, name='article_request'),
]