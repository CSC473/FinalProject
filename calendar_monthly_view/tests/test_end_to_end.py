from calendar_monthly_view.forms import EventForm
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from calendar_monthly_view.models import Event
from datetime import datetime
from calendar_monthly_view.views import event_delete, event_complete
from django.http import HttpRequest
from django.test import Client

class EndToEndTest(TestCase):
    
    def login(self):

        #have a user login 
        c = Client()
        user1 = User.objects.create_user('bob', 'bob@email.com', 'jeff')
        login_in = c.login(username = user1.username, password = user1.password)
        self.assertTrue(login_in)

        # user adds an event 
        self.factory = RequestFactory()
        #brb
        res = Event.objects.get_or_create({
            'user': user1,
            'title': 'Hello',
            'description': 'Bye',
            'end_time' : datetime.now(),
            'start_time': datetime.now(),
            'completed': False,
        })
        obj = Event.objects.filter(id=res[0].id)
        self.assertEqual(obj[0].user.username, "bob")
        self.assertEqual(obj[0].title, "Hello")
        self.assertEqual(obj[0].completed, False)
        self.factory.user = user1

        #user completes the event 
        request = self.factory.post('/complete/'+ str(res[0].id) +'/')
        req1 = event_complete(request, res[0].id)
        self.assertTrue(req1)

        #user deletes event 
        req = event_delete(request, res[0].id)
        self.assertTrue(req)

        #user logout 
        logout_out = c.logout()
        self.assertTrue(logout_out)
