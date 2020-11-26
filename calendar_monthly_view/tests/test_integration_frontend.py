from calendar_monthly_view.forms import EventForm
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from calendar_monthly_view.models import Event
from datetime import datetime
from calendar_monthly_view.views import *
from django.http import HttpRequest
from django.urls import resolve, reverse
from django.test import RequestFactory
from django.test import Client
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin,
)
from django.views.generic import View
from django.contrib import messages
    
class FrontendTesting(TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/account/login/?next=/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))



class CalendarViewTestCase(TestCase):  

    factory = RequestFactory()

    def test_login_required(self):
        view = CalendarView.as_view()
        request = self.factory.get('/monthly_calendar/')
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_login_failed(self):
        view = CalendarView.as_view()
        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account/login/?next=/', response.url)