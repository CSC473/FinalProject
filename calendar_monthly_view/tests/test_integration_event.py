from calendar_monthly_view.forms import EventForm
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from calendar_monthly_view.models import Event
from datetime import datetime
from calendar_monthly_view.views import event_delete, event_complete
from django.http import HttpRequest

class EventIntegrationTest(TestCase):
    def test_event_deletion(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        
        res = Event.objects.get_or_create({
            'user': self.user,
            'title': 'chicken',
            'description': 'noodle',
            'end_time' : datetime.now(),
            'start_time': datetime.now(),
            'completed': False,
        })
        
        self.assertEqual(res[0].user.username, "john")
        self.assertEqual(res[0].title, "chicken")
        self.assertEqual(res[0].completed, False)

        self.factory.user = self.user
        request = self.factory.post('/complete/'+ str(res[0].id) +'/') 

        req1 = event_complete(request, res[0].id)
        self.assertTrue(req1)
        obj = Event.objects.filter(id=res[0].id)
        self.assertTrue(obj[0].completed)

        req = event_delete(request, res[0].id)
        self.assertTrue(req)
        self.assertFalse (Event.objects.filter(id=res[0].id).exists())



