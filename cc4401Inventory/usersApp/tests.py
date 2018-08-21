from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from articlesApp.models import Article
from mainApp.models import User

from loansApp.models import Loan
from reservationsApp.models import Reservation

from PIL import Image
import tempfile
from django.test import override_settings
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import datetime, timedelta

# creates an article instance (fixture)
def create_article(image):
    return Article.objects.create(name='guitarra', description='una guitarra',image=image, state='D')


# creates temporary image for article parameter
def get_temporary_image(temp_file):
    image = Image.new('RGB', (100, 100))
    image.save(temp_file, 'jpeg')
    return temp_file


class UsersTest(TestCase):

    def setUp(self):
        # Set Up
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file)
        self.my_article = create_article(image=test_image.name)
        self.my_article_id = self.my_article.id
        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('12345')
        self.user.save()


        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:01'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')

        self.reservation1 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation1.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:02'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')


        self.reservation2 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation2.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:04'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')


        self.reservation3 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation3.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:06'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')


        self.reservation4 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation4.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:08'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')

        self.reservation5 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation5.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:10'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')


        self.reservation6 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation6.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:12'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')


        self.reservation7 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation7.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:14'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')


        self.reservation8 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation8.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:16'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')


        self.reservation9 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation9.save()

        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:18'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')

        self.reservation10 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation10.save()


        fecha_inicio = '2018-08-10'
        hora_inicio  = '15:20'
        fecha_fin    =  '2018-09-10'
        hora_fin     = '16:30'
        string_inicio = fecha_inicio + ' ' + hora_inicio
        start_date_time = datetime.strptime(string_inicio, '%Y-%m-%d %H:%M')
        string_fin = fecha_fin + ' ' + hora_fin
        final_date_time = datetime.strptime(string_fin, '%Y-%m-%d %H:%M')


        self.reservation11 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation11.save()

        #import pdb
        #pdb.set_trace()
        self.reservation1 = Loan(article=self.my_article, starting_date_time = start_date_time, ending_date_time=final_date_time, user=self.user)
        #self.reservation1_id = self.reservation1.id
        self.reservation1.save()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_model(self):

        self.assertIsNotNone(self.my_article.image)
        self.assertTrue(isinstance(self.my_article, Article))

    def test_have_object(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('user_data', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usersApp/user_profile.html')
        self.assertEqual(len(response.context['articulos1']), 10) # no se han hecho prestamos

        the_article = response.context['articulos1'][0].article
        self.assertEqual(the_article.name, 'guitarra')
        self.assertEqual(the_article.description, 'una guitarra')
        self.assertIsNotNone(the_article.image)
        self.assertEqual(the_article.image, self.my_article.image)
        self.assertEqual(the_article.state, 'D')




    def test_have_order(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('user_data', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usersApp/user_profile.html')
        self.assertEqual(len(response.context['articulos1']), 10) # no se han hecho prestamos

        the_article_time1 = response.context['articulos1'][0].starting_date_time
        the_article_time2 = response.context['articulos1'][1].starting_date_time
        the_article_time3 = response.context['articulos1'][2].starting_date_time

        self.assertTrue(the_article_time2 > the_article_time3)


    def test_eliminate(self):

        self.client.login(email='test@email.com', password='12345')
        url = reverse('delete_loans')
        data = {'loan': self.reservation1.id}
        response = self.client.post(url, data=data)
        url = reverse('delete_loans')
        data = {'loan': self.reservation2.id}
        response = self.client.post(url, data=data)
        url = reverse('delete_loans')
        data = {'loan': self.reservation3.id}
        response = self.client.post(url, data=data)

        url = reverse('user_data', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(len(response.context['articulos1']), 9)

    def test_space_data(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('space_data', args=[self.my_space_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'space_data.html')
# article_data is a login required method -> need to login to reach our article, otherwise renders login.html template

