from django import forms
from .models import TravelOption

class TravelFilterForm(forms.Form):
    TRAVEL_TYPES = [
        ('', 'All Types'),
        ('Flight', 'Flight'),
        ('Train', 'Train'),
        ('Bus', 'Bus'),
    ]
    
    type = forms.ChoiceField(choices=TRAVEL_TYPES, required=False)
    source = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    departure_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}))
    max_price = forms.DecimalField(required=False, min_value=0)

class TravelOptionForm(forms.ModelForm):
    class Meta:
        model = TravelOption
        fields = ['type', 'source', 'destination', 'departure_date', 'departure_time', 'arrival_date', 'arrival_time', 'price', 'available_seats', 'description']
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

