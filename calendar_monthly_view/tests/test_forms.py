from calendar_monthly_view.forms import EventForm
from django.test import TestCase
from django.contrib.auth.models import User
from calendar_monthly_view.models import Event
from datetime import datetime
from calendar_monthly_view.views import event

class EventFormTest(TestCase):
    def test_valid_data(self):
        user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        form = EventForm({
            'user': user1.id,
            'title': 'chicken',
            'description': 'noodle',
            'end_time' : datetime.now(),
            'start_time': datetime.now(),
            'completed': False,
        })
        self.assertTrue(form.is_valid())

    
     
    
        