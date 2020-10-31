from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from calendar_monthly_view.models import * 
from calendar_monthly_view.utils import Calendar 
from .forms import EventForm


class CalendarView(generic.ListView):
    model = Event 
    template_name = 'monthly.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar 
        d = get_date(self.request.GET.get('month', None))

        #Use today's year and date for the Calendar 
        cal = Calendar(d.year, d.month)
        
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal) 

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day = 1)
    return datetime.today()

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        #return HttpResponseRedirect(reverse("calendar_monthly_view:calendar"))
    return render(request, "event.html", {'form': form})


def view_event(request):
    instance = Event.objects.all()
    return render(request, "view_event.html", {'instance': instance})

def event_delete(request, pk):
    instance = get_object_or_404(Event, pk= pk)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect(reverse('view_event'))

    return render(request, "view_event.html")

    

class WeeklyView(generic.ListView):
    model = Event 
    template_name = 'weekly.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar 
        d = get_date(self.request.GET.get('month', None))

        #Use today's year and date for the Calendar 
        cal = Calendar(d.year, d.month)
        
        html_cal = cal.formatweekly(withyear=True)
        events = Event.objects.filter(end_time__year = d.year, end_time__month = d.month)
        context['calendar_week'] = mark_safe(html_cal) 

        #context['prev_week'] = prev_week(d)
        #context['next_week'] = next_week(d)

        return context

