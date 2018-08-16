from django.test import TestCase
from django.urls import reverse
from mainApp.models import User
from articlesApp.models import Article
from spacesApp.models import Space
from reservationsApp.models import Reservation
import datetime


# Create your tests here.
class TestLandingPageUser(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('12345')
        self.user.save()
        self.article1 = Article.objects.create(name='parlante', state='D')
        self.article2 = Article.objects.create(name='alargador', state='P')
        self.article3 = Article.objects.create(name='ak-47', state='P')
        self.space1 = Space(name='quincho', state='P')
        self.space2 = Space(name='multiuso', state='P')
        today = datetime.date.today()
        last_monday = today - datetime.timedelta(days=today.weekday())
        start_time = datetime.time(hour=12, minute=00)
        end_time = datetime.time(hour=15, minute=00)
        start_datetime1 = datetime.datetime.combine(last_monday, start_time)
        end_datetime1 = datetime.datetime.combine(last_monday, end_time)
        self.reservation1 = Reservation(space=self.space1, user=self.user, state='A',
                                        starting_date_time=start_datetime1, ending_date_time=end_datetime1)
        last_tuesday = today - datetime.timedelta(days=(today.weekday()-1))
        start_datetime2 = datetime.datetime.combine(last_tuesday, start_time)
        end_datetime2 = datetime.datetime.combine(last_tuesday, end_time)
        self.reservation2 = Reservation(space=self.space2, user=self.user, state='A',
                                        starting_date_time=start_datetime2, ending_date_time=end_datetime2)
        print(start_datetime1)
        print(start_datetime2)

    def test_calendar(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('landing_spaces')
        response = self.client.get(url)
        print(response.context['reservations'])

    def test_search_articles_name(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('search')
        data = {'query': 'parlante', 'tipo': '', 'estado': 'A'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos.html')
        self.assertEqual(len(response.context['productos']), 1)
        self.assertEqual(response.context['productos'][0].name, 'parlante')

    def test_search_articles_state(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('search')
        data = {'query': '', 'tipo': '', 'estado': 'P'}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articulos.html')
        self.assertEqual(len(response.context['productos']), 2)
        self.assertEqual(response.context['productos'][0].name, 'alargador')
        self.assertEqual(response.context['productos'][1].name, 'ak-47')
