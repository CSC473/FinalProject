from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
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
        res = form.save()
        assert res.is_active, "registration failed"

        c = Client()
        logged_in = c.login(username='testingcode', password='error777')
        self.assertTrue(logged_in)


    def test_registration_fail(self):
        form = RegisterForm({
            'username': 'testingcode',
            'email': 'testing',
            'password1' : "error77",
            'password2': "error77",
        })
        self.assertFalse(form.is_valid())

        c = Client()
        logged_in = c.login(username='testingcode', password='error77')
        self.assertFalse(logged_in)



