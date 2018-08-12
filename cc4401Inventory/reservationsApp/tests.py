from django.test import TestCase
from django.test import Client
from articlesApp.models import Article
from loansApp.models import Loan
from mainApp.models import User
from datetime import datetime, timedelta
# Create your tests here.


class TestTemplate(TestCase):
    def setUp(self):
        user = User.objects.create(email='user@user.user', first_name='Bob', last_name='Esponja', rut='11.111.111-1')
        article1 = Article.objects.create(name='Parlante', state='Disponible')
        article2 = Article.objects.create(name='Alargador', state='Disponible')
        Loan.objects.create(article=article1, user=user, state='Pendiente',
                            starting_date_time=datetime.now(),
                            ending_date_time=(datetime.now() + timedelta(days=1)))
        Loan.objects.create(article=article2, user=user, state='Pendiente',
                            starting_date_time=datetime.now(),
                            ending_date_time=(datetime.now() + timedelta(days=1)))

    def test_get_articles(self):
        article = Article.objects.get(name='Parlante')
        self.assertEqual(article.state, 'Disponible')
