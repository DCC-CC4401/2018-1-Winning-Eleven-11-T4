from django.test import TestCase
from spacesApp.models import Space
from articlesApp.models import Article
from mainApp.models import User
from reservationsApp.models import Reservation
from loansApp.models import Loan
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import datetime, timedelta

class AdminTest(TestCase):

    def setUp(self):
        date_in1 = datetime(2018, 8, 29, 12, 00)
        date_in2 = datetime(2018, 8, 30, 12, 00)
        date_fin1 = datetime(2018, 8, 29, 13, 00)
        date_fin2 = datetime(2018, 8, 30, 13, 00)
        self.article = Article.objects.create(name='guitarra', description='una guitarra', state='D')
        self.space = Space.objects.create(name='Espacio1', description='un espacio', state='D')
        self.user = User.objects.create(email='test@email.com', is_staff=True, is_superuser=True)
        self.user.set_password('12345')
        self.user.save()
        #reserva 1 el 29/08/2018 desde 12pm a 13pm
        #reserva 2 el 30/08/2018 desde 12pm a 13pm
        #Se agrega la reserva2 antes que la reserva1
        self.reservation2 = Reservation.objects.create(space=self.space, starting_date_time=date_in2,
                                      ending_date_time=date_fin2, user=self.user)
        self.reservation1 = Reservation.objects.create(space=self.space, starting_date_time=date_in1,
                                      ending_date_time=date_fin1, user=self.user)
        #prestamo 1 el 29/08/2018 desde 12pm a 13pm, perdido
        #prestamo 2 el 30/08/2018 desde 12pm a 13pm, caducado
        #Se agrega el loan2 antes que el loan1
        self.loan2 = Loan.objects.create(article=self.article, starting_date_time=date_in2,
                                      ending_date_time=date_fin2, user=self.user, state='L')
        self.loan1 = Loan.objects.create(article=self.article, starting_date_time=date_in1,
                                      ending_date_time=date_fin1, user=self.user, state='P')



    def test_pend_reservations_ordered_by_starting_date_time(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('actions-panel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'actions_panel.html')
        reservations = response.context['reservations_query']
        #se ordenan por fecha de inicio
        self.assertEqual(reservations[0], self.reservation1)
        self.assertEqual(reservations[1], self.reservation2)

    def test_loans_ordered_by_starting_date_time(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('actions-panel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'actions_panel.html')
        loans = response.context['loans']
        #se ordenan por fecha de inicio
        self.assertEqual(loans[0], self.loan1)
        self.assertEqual(loans[1], self.loan2)

    def test_loans_filtered_caducados(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('actions-panel')
        response = self.client.get(url, {'filter': 'caducados'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'actions_panel.html')
        loans = response.context['loans']
        #solo hay uno caducado
        self.assertEqual(self.loan1.state,'P')
        self.assertEqual(loans[0], self.loan1)

    def test_loans_filtered_perdidos(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('actions-panel')
        response = self.client.get(url, {'filter': 'perdidos'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'actions_panel.html')
        loans = response.context['loans']
        #solo hay uno perdido
        self.assertEqual(self.loan2.state,'L')
        self.assertEqual(loans[0],self.loan2)

    def test_loans_filtered_vigentes(self):
        self.client.login(email='test@email.com', password='12345')
        url = reverse('actions-panel')
        response = self.client.get(url, {'filter':'vigentes'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'actions_panel.html')
        loans = response.context['loans']
        #no hay vigentes
        self.assertEqual(len(loans),0)

    def test_check_pend_reservations_and_accept_one(self):
        self.client.login(email='test@email.com', password='12345')
        selected = [self.reservation1.id]
        url = reverse('modify_reservations')
        data = {
            'selected': selected,
            'accept': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        reserv1modified = Reservation.objects.get(id=self.reservation1.id)
        self.assertEqual(reserv1modified.id,self.reservation1.id)
        self.assertEqual(reserv1modified.state, 'A')

    def test_check_pend_reservations_and_refuse_one(self):
        self.client.login(email='test@email.com', password='12345')
        selected = [self.reservation2.id]
        url = reverse('modify_reservations')
        data = {
            'selected': selected,
            'accept': 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        reserv2modified = Reservation.objects.get(id=self.reservation2.id)
        self.assertEqual(reserv2modified.id, self.reservation2.id)
        self.assertEqual(reserv2modified.state, 'R')

    def test_check_pend_reservations_and_accept_two(self):
        self.client.login(email='test@email.com', password='12345')
        selected = [self.reservation1.id, self.reservation2.id]
        url = reverse('modify_reservations')
        data = {
            'selected': selected,
            'accept': 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        reserv1modified = Reservation.objects.get(id=self.reservation1.id)
        reserv2modified = Reservation.objects.get(id=self.reservation2.id)
        self.assertEqual(reserv1modified.id,self.reservation1.id)
        self.assertEqual(reserv2modified.id, self.reservation2.id)
        self.assertEqual(reserv1modified.state, 'A')
        self.assertEqual(reserv2modified.state, 'A')
