from django.test import TestCase
from django.urls import reverse
from articlesApp.models import Article
from mainApp.models import User

# Create your tests here.


class TestArticles(TestCase):
    def setUp(self):

        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('12345')
        self.user.save()

