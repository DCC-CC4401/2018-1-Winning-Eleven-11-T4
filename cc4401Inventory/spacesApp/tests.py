from django.test import TestCase
from spacesApp.models import Space
from mainApp.models import User
from PIL import Image
import tempfile
from django.test import override_settings
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import datetime, timedelta


# creates space instance (fixture)
def create_space(image):
    return Space.objects.create(name='auditorio', description='un auditorio',image=image, state='D', capacity=300)


# creates temporary image for space parameter
def get_temporary_image(temp_file):
    image = Image.new('RGB', (100, 100))
    image.save(temp_file, 'jpeg')
    return temp_file


class SpaceTest(TestCase):

    def setUp(self):
        # Set Up
        temp_file = tempfile.NamedTemporaryFile()
        self.test_image = get_temporary_image(temp_file)
        self.my_space = create_space(image=self.test_image.name)
        self.my_space_id = self.my_space.id

        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('12345')
        self.user.save()

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_model(self):

        self.assertIsNotNone(self.my_space.image)
        self.assertTrue(isinstance(self.my_space, Space))


# space_data is a login required method -> need to login to reach our space, otherwise renders login.html template
    def test_space_data_view_without_login(self):

        url = reverse('space_data', args=[self.my_space_id])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/user/login/?next=/space/%d/' % self.my_space_id)
        self.assertTemplateUsed(response, 'usersApp/login.html')

    def test_space_data_view_with_user(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('space_data', args=[self.my_space_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'space_data.html')
        self.assertEqual(len(response.context['reservations']), 0)    # no se han hecho prestamos
        the_space = response.context['space']
        self.assertEqual(the_space.name, 'auditorio')
        self.assertEqual(the_space.description, 'un auditorio')
        self.assertIsNotNone(the_space.image)
        self.assertEqual(the_space.image, self.my_space.image)
        self.assertEqual(the_space.state, 'D')
        self.assertEqual(the_space.capacity, 300)

    def test_space_data_view_exito(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('space_data', args=[self.my_space_id])
        data = {'startDate': '2018-08-21 14:30', 'endDate': '2018-08-21 15:30'}

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_space_edit_fields_success(self):
        admin = User.objects.create_superuser(email='admin@cei.cl', password='12345')
        admin.is_staff = True
        self.client.login(email=admin.email, password='12345')

        self.assertEqual(self.my_space.name, 'auditorio')
        self.assertEqual(self.my_space.description, 'un auditorio')
        self.assertEqual(self.my_space.image, self.test_image.name)
        self.assertEqual(self.my_space.state, 'D')
        self.assertEqual(self.my_space.capacity, 300)

        url = reverse('space_edit_fields', args=[self.my_space_id])
        form_data = {'name': 'nuevo nombre', 'state': 'P', 'image': False,
                     'description': 'nueva decripcion', 'capacity': 400}
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Espacio editado exitosamente')

    def test_space_edit_fields_fail(self):
        admin = User.objects.create_superuser(email='admin@cei.cl', password='12345')
        admin.is_staff = True
        self.client.login(email=admin.email, password='12345')

        self.assertEqual(self.my_space.name, 'auditorio')
        self.assertEqual(self.my_space.description, 'un auditorio')
        self.assertEqual(self.my_space.image, self.test_image.name)
        self.assertEqual(self.my_space.state, 'D')
        self.assertEqual(self.my_space.capacity, 300)

        url = reverse('space_edit_fields', args=[self.my_space_id])
        # form_data capacity field missing
        form_data = {'name': 'nuevo nombre', 'state': 'P', 'image': False,
                     'description': 'nueva decripcion'}
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Error al editar')