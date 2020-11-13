#Test file to test model behavior of calendar
from calendar_monthly_view.models import Event
from django.test import TestCase
from django.contrib.auth.models import User


class EventModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Set up non-modified objects used by all test methods
        user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        Event.objects.create(user_id=user1.id, title='bob',start_time='2020-10-10',end_time='2020-10-10')

    def test_title_max_length(self):
        title_event = Event.objects.get(user_id=1)
        max_length = title_event._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)
    

 
    