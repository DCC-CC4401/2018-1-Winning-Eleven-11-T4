from django.test import TestCase
from test_base import BaseLoggedIn
from .models import Reservation

# Create your tests here.


class BaseReservation(BaseLoggedIn):
    def setUp(self):
        super().setUp()


    def reservation_created(self):
        pass
