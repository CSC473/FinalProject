from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from register.forms import RegisterForm
from register.models import UserProfile
from django.contrib import auth
from django.test import Client
from register.views import register
from calendar_monthly_view.views import view_event

class SignUpTests(TestCase):
    def test_signup_status_code(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/register/')
        self.assertEquals(view.func, register)

    def test_view_events(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        logged_in = self.client.login(username='john', password='johnpassword')
        url = reverse('view_event')
        response = self.client.get(url)
        #self.assertValidResponse(response)
        self.assertEquals(response.status_code, 200)

    def test_events(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        logged_in = self.client.login(username='john', password='johnpassword')
        url = reverse('event')
        response = self.client.get(url)
        #self.assertValidResponse(response)
        self.assertEquals(response.status_code, 200)
    




