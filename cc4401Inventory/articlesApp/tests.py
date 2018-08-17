from django.test import TestCase
from articlesApp.models import Article
from mainApp.models import User
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


class ArticleTest(TestCase):

    def setUp(self):
        # Set Up
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file)
        self.my_article = create_article(image=test_image.name)
        self.my_article_id = self.my_article.id
        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('12345')
        self.user.save()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_model(self):

        self.assertIsNotNone(self.my_article.image)
        self.assertTrue(isinstance(self.my_article, Article))


# article_data is a login required method -> need to login to reach our article, otherwise renders login.html template
    def test_article_data_view_without_login(self):

        url = reverse('article_data', args=[self.my_article_id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/user/login/?next=/article/%d/' % self.my_article_id)
        self.assertTemplateUsed(response, 'usersApp/login.html')

    def test_article_data_view_with_user(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('article_data', args=[self.my_article_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_data.html')
        self.assertEqual(len(response.context['last_loans']), 0) # no se han hecho prestamos
        the_article = response.context['article']
        self.assertEqual(the_article.name, 'guitarra')
        self.assertEqual(the_article.description, 'una guitarra')
        self.assertIsNotNone(the_article.image)
        self.assertEqual(the_article.image, self.my_article.image)
        self.assertEqual(the_article.state, 'D')

    def test_article_request_view_exito(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('article_request')
        data = {'article_id': self.my_article_id,
                'fecha_inicio': '2018-09-10', 'hora_inicio': '14:30', 'fecha_fin': '2018-09-10', 'hora_fin': '15:30'}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Pedido realizado con éxito')

    def test_article_rquest_view_horario_habil(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('article_request')
        data = {'article_id': self.my_article_id,
                'fecha_inicio': '2018-09-10', 'hora_inicio': '07:30', 'fecha_fin': '2018-09-10', 'hora_fin': '19:30'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Los pedidos deben ser hechos en horario hábil.')

    def test_article_rquest_view_horario_hora_anticipacion(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('article_request')
        data = {'article_id': self.my_article_id,
                'fecha_inicio': '2018-08-10', 'hora_inicio': '15:00', 'fecha_fin': '2018-09-10', 'hora_fin': '16:30'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Los pedidos deben ser hechos al menos con una hora de anticipación.')

    def test_article_rquest_view_horario_devolucion(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('article_request')
        data = {'article_id': self.my_article_id,
                'fecha_inicio': '2018-09-10', 'hora_inicio': '14:30', 'fecha_fin': '2018-10-10', 'hora_fin': '15:30'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Los pedidos deben ser devueltos el mismo día que se entregan.')

    def test_article_rquest_view_horario_fecha_correcta(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('article_request')
        data = {'article_id': self.my_article_id,
                'fecha_inicio': '2018-09-10', 'hora_inicio': '14:30', 'fecha_fin': '2018-09-09', 'hora_fin': '15:30'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'La reserva debe terminar después de iniciar.')

    # def test_article_rquest_view_usuario_habilitado(self):
    #     self.client.login(email='test@email.com', password='12345')
    #     user_status = self.user.enabled
    #     url = reverse('article_request')
    #     data = {'article_id': self.my_article_id,
    #             'fecha_inicio': '2018-09-10', 'hora_inicio': '14:30', 'fecha_fin': '2018-09-10', 'hora_fin': '15:30'}
    #     response = self.client.post(url, data=data)
    #     self.assertEqual(response.status_code, 302)
    #
    #     messages = list(get_messages(response.wsgi_request))
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(str(messages[0]), 'Usuario no habilitado para pedir préstamos')























class TestArticles(TestCase):
    def setUp(self):

        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('12345')
        self.user.save()

