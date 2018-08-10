from django.test import TestCase
from test_base import BaseLoggedIn, BaseArticle
from datetime import datetime
from loansApp.models import Loan
from django.test import Client
from django.contrib.messages import get_messages


# Create your tests here.

def to_datetime(self, datestring):
	return datetime.strptime(datestring, '%Y-%m-%d %H:%M')

class BaseLoan(BaseLoggedIn, BaseArticle):

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
		super(BaseLoggedIn, self)
		super(BaseArticle, self)
		#super()

		self.loan = self.create_a_loan(self.get_article_foo())
		self.loans = []
		# Loan creation by post

	def test_loan_was_saved(self):
		fecha_inicio = '2018-08-30'
		hora_inicio = '13:00'
		fecha_fin = '2018-09-01'
		hora_fin = '13:00'
		article_id = self.get_article_foo().id
		c = Client()
		response = c.post('/article/request', {
			'fecha_inicio': fecha_inicio,
			'hora_inicio': hora_inicio,
			'fecha_fin': fecha_fin,
			'hora_fin': hora_fin,
			'article_id': article_id
		})

		err = [str(e) for e in get_messages(response.wsgi_request)]

		self.assertIn('Pedido realizado con éxito', err)









