from datetime import datetime, timedelta 
from calendar import HTMLCalendar 
from calendar_monthly_view.models import Event

class Calendar(HTMLCalendar):
    def __init__(self, year = None, month =None):
        self.year = year 
        self.month = month 
        super(Calendar, self).__init__()

    #formats a day as a td 
    #filter events by day 
    def formatday(self, day, events):
        events_per_day = events.filter(end_time__day=day)
        d = ''
        for event in events_per_day: 
            d += f'<li> {event.title} </li>'

        if day != 0: 
            return f'<td><span class="date">{day}</span><ul> {d} </ul></td>'
        return '<td></td>'

    #format week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    #format a month as a table 
    def formatmonth(self, withyear = True):
        events = Event.objects.filter(end_time__year = self.year, end_time__month = self.month)
        cal = f'<table border = "0" cellpadding = "0" cellspacing = "0" class = "calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal 

    def formatweekly(self, withyear = True):
        events = Event.objects.filter(end_time__year = self.year, end_time__month = self.month)
        cal = f'<table border = "0" cellpadding = "0" cellspacing = "0" class = "calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
       
        current_time = datetime.now() # get current day 
        current = int(current_time.strftime('%d')) # convert day # to int
        for week in self.monthdays2calendar(self.year, self.month):
            for day in week:
                date = int(str(day[0]))
                if date == current:
                    cal += f'{self.formatweek(week, events)}\n'
        return cal

    