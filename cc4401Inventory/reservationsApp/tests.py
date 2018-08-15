from django.test import TestCase
from django.urls import reverse
from articlesApp.models import Article
from loansApp.models import Loan
from mainApp.models import User
from datetime import datetime, timedelta
# Create your tests here.


class ArticleSearchTest(TestCase):
    def setUp(self):
        self.article1 = Article.objects.create(name='parlante', state='D')
        self.article2 = Article.objects.create(name='alargador', state='P')
        self.article3 = Article.objects.create(name='ak-47', state='L')
        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('12345')
        self.user.save()

    def test_search_articles(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('search')
        data = {'query': 'parlante', 'tipo': '', 'estado': 'D'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos.html')
        print(response.context['productos'])
