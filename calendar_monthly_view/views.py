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
from django.contrib import messages

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
    #print(month)
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
        
        return HttpResponseRedirect(reverse("calendar"))
    return render(request, "event.html", {'form': form})

def view_event(request):
    instance = Event.objects.filter(user=request.user)
    complete = Event.objects.filter(user=request.user, completed = True)
    complete_count = 0
    for c in complete:
        complete_count += 1

    past_count = 0
    in_count = 0

    now = datetime.today().date()
    past = Event.objects.filter(user=request.user, completed= False, end_time__lte = now)
    for p in past:
        past_count +=1

    inprogress = Event.objects.filter(user=request.user, completed= False, end_time__gte = now)
    for i in inprogress:
        in_count += 1
    labels = ['In Progress', 'Complete', 'Past-Due']
    data = [in_count,complete_count, past_count]
    total = in_count + complete_count + past_count
    context = {
        'instance': instance,
        'labels': labels,
        'data':data,
        'in_prog': data[0],
        'cd': data[1],
        'pd': data[2],
        'total': total,
    }
   
    return render(request, "view_event.html",context)

def event_delete(request, pk):
    instance = get_object_or_404(Event, pk= pk)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, 'You have 0 tasks due today')
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
        context['instance'] = Event.objects.filter(user=self.request.user)

        context['calendar_week'] = mark_safe(html_cal_week) 

        now = datetime.today().date()
        past = Event.objects.filter(user=self.request.user, completed= False, end_time__lte = now)
        num = 0
        for p in past:
            num +=1

        messages.info(self.request, 'Notification: You have ' + str(num) + ' tasks due today!')

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
        
