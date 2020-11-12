from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from calendar import HTMLCalendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import * 
from .utils import Calendar 
from .forms import EventForm

class CalendarView(LoginRequiredMixin,generic.ListView):
    login_url = 'login'
    model = Event 
    template_name = 'monthly.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarView,self).get_context_data(**kwargs)

        # use today's date for the calendar 
        d = get_date(self.request.GET.get('month', None))

        # Filter the instances based on the user
        context['instance'] = Event.objects.filter(user=self.request.user)
        user = self.request.user.id
        #Use today's year and date for the Calendar 
        cal = Calendar(d.year, d.month, user)
    
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
    print(month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day = 1)
    return datetime.today()

@login_required(login_url='login')
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        #form.save()
        return HttpResponseRedirect(reverse("calendar"))
    return render(request, "event.html", {'form': form})

def view_event(request):
    instance = Event.objects.filter(user=request.user)
    return render(request, "view_event.html", {'instance': instance})

def event_delete(request, pk):
    instance = get_object_or_404(Event, pk= pk)
    if request.method == 'POST':
        instance.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    #return render(request, "view_event.html")


class WeeklyView(LoginRequiredMixin,generic.ListView):
    login_url = 'login'
    model = Event 
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar 
        d = get_date(self.request.GET.get('month', None))
        d = d.replace(day=int(datetime.now().strftime('%d')))
        user = self.request.user.id
        #Use today's year and date for the Calendar 
        cal = Calendar(d.year, d.month, user)
        
        html_cal_week = cal.formatweekly(d, withyear=True)
        #events = Event.objects.filter(end_time__year = d.year, end_time__month = d.month)
        #context['instance'] = Event.objects.filter(user=self.request.user)

        context['calendar_week'] = mark_safe(html_cal_week) 

        context['prev_week'] = prev_week(d)
        context['next_week'] = next_week(d)

        return context


def event_complete(request, pk):
    instance = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        if instance.completed == False: #if task completed, change to true
            instance.completed = True
            instance.save(update_fields=['completed'])
        else:
            instance.completed = False
            instance.save(update_fields=['completed'])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def event_stats(request):
    instance = Event.objects.filter(user=request.user)
    return render(request, "profile.html")
        

def prev_week(d):
    prev_week = d - timedelta(days=7)
    week = 'month=' + str(prev_week.year) + '-' + str(prev_week.month)
    day = 'day=' + "1 2 3 4 5 6 7"
    return day 

def next_week(d):
    next_week = d + timedelta(days=7)
    #cal = Calendar(d.year, d.month)
    #html_cal_week = cal.formatweekly(next_week, withyear=True)
    week = "date=" + str(next_week.year) + '-' + str(next_week.month) + '-' + str(next_week.day)
    print(week)
    return next_week


