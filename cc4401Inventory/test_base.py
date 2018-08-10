from django.test import TestCase
from mainApp.models import User
from articlesApp.models import Article
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages

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

        self.user_foo.save()



    def get_user_foo(self):
        return User.objects.get(email=email)


class LoggedIn(BaseLoggedIn):
    def setUp(self):
        super().setUp()

    def test_created_user(self):
        foo_user = User.objects.get(email=email)
        self.assertEqual("fooFirstName", foo_user.first_name)
        self.assertEqual("fooFirstName", self.user_foo.first_name)


    def test_logged_user(self):
        self.assertEqual(self.response_login.context['user'].email, email)

    def test_post_login(self):
        c = Client()
        login_submit_url = '/user/login/submit/'

        response = c.post(login_submit_url, {'email': self.user_foo.email,
                                             'password': passwd})

        #err = list(get_messages(response.wsgi_request))
        #print(response)
        #print([str(e) for e in err])

        self.assertEqual(response.url, '/articles/')


class BaseArticle(TestCase):

    def create_an_article(self):
        if not hasattr(self, 'article') or self.articles is None:
            self.articles = []

        article = Article(state='D', name="FooArticle %d" % len(self.articles),
                          description="FooArticle %d description" % len(self.articles))

        self.articles.append(article)

        return article

    def get_article_foo(self):
        if not hasattr(self, 'article') or self.article is None:
            self.article = self.create_an_article()
        return self.article

    def setUp(self):
        self.articles = []
        self.article = self.get_article_foo()
