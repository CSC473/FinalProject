from django.test import TestCase, RequestFactory
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from .views import register
from register.forms import RegisterForm
from register.models import UserProfile
from django.contrib import auth
from django.test import Client
from register.views import register

class RegisterFormTest(TestCase):
    def test_registration_success(self):
        form = RegisterForm({
            'username': 'testingcode',
            'email': 'testing@gmail.com',
            'password1' : "error777",
            'password2': "error777",
        })
        self.assertTrue(form.is_valid())


class SignUpTests(TestCase):
    def test_signup_status_code(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/register/')
        self.assertEquals(view.func, register)
