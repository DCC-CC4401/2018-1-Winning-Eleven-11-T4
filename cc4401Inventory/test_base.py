from django.test import TestCase
from mainApp.models import User


email = "foo@bar.com"
passwd = "wenawena"

class BaseLoggedIn(TestCase):
    def setUp(self):
        self.user_foo = User.objects.create_user(first_name="fooFirstName",
                                        last_name="fooLastName",
                                        email=email,
                                        password=passwd,
                                        rut="123456789")

        self.client.login(email=email, password=passwd)
        self.response_login = self.client.get("/", follow=True)


class LoggedIn(BaseLoggedIn):
    def setUp(self):
        super().setUp()

    def test_created_user(self):
        foo_user = User.objects.get(email="foo@bar.com")
        self.assertEqual("fooFirstName", foo_user.first_name)
        self.assertEqual("fooFirstName", self.user_foo.first_name)

    def test_logged_user(self):
        self.assertEqual(self.response_login.context['user'].email, email)
