from django.forms import ModelForm, DateInput, CheckboxInput
from calendar_monthly_view.models import Event
from django import forms

class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'completed': CheckboxInput(attrs={'type': 'checkbox'})
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['completed'] = forms.BooleanField(required=False)