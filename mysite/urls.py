"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import TemplateView # new
from register import views as v
from calendar_monthly_view import views
from user_profile import views as up

urlpatterns = [
    path('', views.WeeklyView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('account/', include('django.contrib.auth.urls')),
    path('monthly_calendar/', views.CalendarView.as_view(), name ='calendar'),

    path('profile/', views.view_event, name='view_event'),
    path('register/', v.register, name='register'),
    path('event/', views.event, name='event'),
    path('event_edit/', include('calendar_monthly_view.urls'), name='event_edit'),

    url(r'^delete/(?P<pk>[0-9]+)/$', views.event_delete, name='event_delete'),
    url(r'^complete/(?P<pk>[0-9]+)/$', views.event_complete, name='event_complete'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.event_delete, name='event_delete'),
]
