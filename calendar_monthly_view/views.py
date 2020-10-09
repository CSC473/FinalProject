from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import * 
from .utils import Calendar 

class CalendarView(generic.ListView):
    model = Event 
    template_name = 'monthly.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar 
        d = get_date(self.request.GET.get('day', None))

        #Use today's year and date for the Calendar 
        cal = Calendar(d.year, d.month)

        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal) 
        return context
    

def monthlyView(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day = 1)
    return datetime.today()
