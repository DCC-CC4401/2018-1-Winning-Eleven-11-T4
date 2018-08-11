from django.test import TestCase
from test_base import BaseLoggedIn, BaseArticle
from datetime import datetime, timedelta
from loansApp.models import Loan
from django.contrib.messages import get_messages

from utils.time_utils import to_chile_time_normalization, is_non_workday
from django.test import tag


class BaseLoan(BaseLoggedIn, BaseArticle):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.loans = []

	def create_a_loan(self, article=None):
		if article is None:
			article = self.create_an_article()

		start_date_time = datetime.now()
		end_date_time = datetime.now()
		loan = Loan(article=article,
					starting_date_time=start_date_time,
					ending_date_time=end_date_time,
					user=self.get_user_foo())
		if self.loans is None:
			self.loans = []

		self.loans.append(loan)
		return loan

	def setUp(self):
		super(BaseLoggedIn, self).setUp()
		super(BaseArticle, self).setUp()

		self.loan = self.create_a_loan(self.get_article_foo())
		self.loans = []


def build_loan_post_object(datetime_start, datetime_end, article_id):
	return {
		'fecha_inicio': str(datetime_start.date()),
		'hora_inicio': str(datetime_start.strftime('%H:%M')),
		'fecha_fin': str(datetime_end.date()),
		'hora_fin': str(datetime_end.strftime('%H:%M')),
		'article_id': article_id
	}

@tag('req7,8,12,14')
class LoansCreationTest(BaseLoan, TestCase):
	def setUp(self):
		super(BaseLoan, self).setUp()
		self.article_id = str(self.get_article_foo().id)

	def send_post(self, to_post):
		response = self.client.post('/article/request', to_post)
		err = [str(e) for e in get_messages(response.wsgi_request)]
		return response, err


	# Testea el requisito 7 (Requisitos Generales)
	def test_loan_was_saved(self):
		fecha_inicio = datetime.now().replace(hour=16, minute=0, second=0, microsecond=0) + timedelta(days=5)
		start_date = to_chile_time_normalization(fecha_inicio)

		fecha_fin = fecha_inicio + timedelta(days=5, hours=1)
		end_date = to_chile_time_normalization(fecha_fin)
		#article_id = str(self.get_article_foo().id)
		to_post = build_loan_post_object(start_date, end_date, self.article_id)
		print(to_post)

		response, err = self.send_post(to_post)

		self.assertIn('Pedido realizado con éxito', err)
		loan_made = Loan.objects.get(id=self.article_id)
		self.assertEqual(loan_made.starting_date_time, start_date)
		self.assertEqual(loan_made.ending_date_time, end_date)
		self.assertEqual(loan_made.user, self.user_foo)

	# Testea el requisito 12 (Requisitos Generales)
	def test_loan_before_one_hour_fails(self):
		for i in range(0, 5):
			now_time = datetime.now() - timedelta(days=i)
			start_date = to_chile_time_normalization(now_time)
			end_date = to_chile_time_normalization(now_time + timedelta(hours=1))
			to_post = build_loan_post_object(start_date, end_date, self.article_id)

			response, err = self.send_post(to_post)

			self.assertIn('Los pedidos deben ser hechos al menos con una hora de anticipación.', err)

	def test_restricted_work_hours(self):
		less_than_9 = datetime.now().replace(hour=8, minute=59, second=59)
		more_than_18 = datetime.now().replace(hour=18, minute=0, second=1)
		rhlist = [less_than_9, more_than_18]
		for rhour in rhlist:
			start_date = to_chile_time_normalization(rhour)
			end_date = to_chile_time_normalization(rhour + timedelta(seconds=5))
			to_post = build_loan_post_object(start_date, end_date, self.article_id)
			response, err = self.send_post(to_post)
			self.assertIn('Los pedidos deben ser hechos en horario hábil.', err)

	def test_restricted_work_days(self):
		now = datetime.now()
		this_year = now.year
		this_month = now.month
		this_weekday = now.weekday()
		new_year = datetime(this_year + 1, 1, 1, hour=16, minute=0, second=0)
		sunday = now.replace(hour=16, minute=0, second=0) + timedelta(days=6-this_weekday)
		saturday = now.replace(hour=16, minute=0, second=0) + timedelta(days=5-this_weekday)
		fiestas_patrias = datetime(this_year + 1, 9, 18, hour=16, minute=0, second=0)
		nwdays = [new_year, sunday, saturday, fiestas_patrias]

		for a_day in nwdays:
			self.assertTrue(is_non_workday(a_day))
			start_date = to_chile_time_normalization(a_day)
			end_date = to_chile_time_normalization(a_day + timedelta(hours=1))
			to_post = build_loan_post_object(start_date, end_date, self.article_id)
			response, err = self.send_post(to_post)
			self.assertIn('Los pedidos deben ser hechos en horario hábil.', err)



