from django.test import TestCase
from django.urls import reverse
from articlesApp.models import Article
from mainApp.models import User
from PIL import Image
import tempfile
from django.contrib.messages import get_messages

class UserCreatedTest(TestCase):
    def setUp(self):

        self.users_before = list(User.objects.values_list('id', flat=True).order_by('id'))
        self.user = User.objects.create(email='test@email.com',first_name='Solid',last_name='Snake',rut=111111111, is_staff=False)
        self.user.set_password('12345678')
        self.user.save()
        self.users_after = list(User.objects.values_list('id', flat=True).order_by('id'))

    def test_user_was_created(self):

        self.assertTrue(isinstance(self.user, User))
        self.assertNotEqual(self.users_before, self.users_after)



class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@email.com',first_name='Solid',last_name='Snake',rut=111111111, is_staff=False)
        self.user.set_password('12345678')
        self.user.save()


    def test_user_was_created(self):
        self.client.login(email='test@email.com', password='12345678')
        url = reverse('landing_articles')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)


class UserTypesTest(TestCase):
    def setUp(self):

        self.user = User.objects.create(email='test@email.com',first_name='Solid',last_name='Snake',rut=111111111,
                                        is_staff=False,is_superuser=False)
        self.user.set_password('12345678')
        self.user.save()

        self.adminuser = User.objects.create(email='testadminuser@email.com', first_name='Venom', last_name='Snake', rut=222222222,
                                        is_staff=True, is_superuser=True)
        self.adminuser.set_password('12345678')
        self.adminuser.save()


    def test_user_was_created(self):

        self.assertTrue(isinstance(self.user, User))
        self.assertTrue(isinstance(self.adminuser, User))
        self.assertNotEqual(self.user.is_staff,self.adminuser.is_staff)
        self.assertNotEqual(self.user.is_superuser, self.adminuser.is_superuser)

def create_article(image):
    return Article.objects.create(name='guitarra', description='una guitarra', image=image, state='D')

def get_temporary_image(temp_file):
    image = Image.new('RGB', (100, 100))
    image.save(temp_file, 'jpeg')
    return temp_file

class ReservationTest(TestCase):


    def setUp(self):
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file)
        self.my_article = create_article(image=test_image.name)
        self.my_article_id = self.my_article.id
        self.user = User.objects.create(email='test@email.com', first_name='Solid', last_name='Snake', rut=111111111,
                                        is_staff=False, is_superuser=False)
        self.user.set_password('12345678')
        self.user.save()

    def test_article_request_view_exito(self):
        self.client.login(email='test@email.com', password='12345678')
        url = reverse('article_request')
        data = {'article_id': self.my_article_id,
                'fecha_inicio': '2018-10-11', 'hora_inicio': '10:30', 'fecha_fin': '2018-10-11', 'hora_fin': '17:30'}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Pedido realizado con éxito')