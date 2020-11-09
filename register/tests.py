from django.test import TestCase
from django.urls import resolve, reverse
from .views import register

# Create your tests here.
from django.contrib.auth.models import User
class SignUpTests(TestCase):
    def test_signup_status_code(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/register/')
        self.assertEquals(view.func, register)
