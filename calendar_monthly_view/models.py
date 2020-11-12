from django.db import models
from django.urls import reverse
from django import forms
from datetime import datetime
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, default="1", on_delete= models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    end_time = models.DateTimeField()
    start_time = models.DateTimeField()
    completed = models.BooleanField(default=False)


    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

    @property
    def is_past_due(self):
    	now = datetime.today().date()
    	due = self.end_time.date()
    	return now > due

    