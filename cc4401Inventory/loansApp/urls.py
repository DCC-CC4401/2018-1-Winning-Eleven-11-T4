from django.urls import path

from . import views

urlpatterns = [
    path('<int:loan_id>', views.loan_data, name='loan_data'),
    path('<int:loan_id>/change_article_state', views.loan_change_article_state, name='change_article_state'),
]
