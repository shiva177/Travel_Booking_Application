from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, TravelOption

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class TravelSearchForm(forms.Form):
    TRAVEL_TYPES = (
        ('', 'All Types'),
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    )
    
    travel_type = forms.ChoiceField(choices=TRAVEL_TYPES, required=False)
    source = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('num_seats',)
        
    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.travel_option:
            self.fields['num_seats'].widget.attrs.update({
                'max': self.travel_option.available_seats,
                'min': 1
            })
    
    def clean_num_seats(self):
        num_seats = self.cleaned_data.get('num_seats')
        if self.travel_option and num_seats > self.travel_option.available_seats:
            raise forms.ValidationError(f"Only {self.travel_option.available_seats} seats available.")
        return num_seats
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.user = self.user
        booking.travel_option = self.travel_option
        booking.total_price = self.travel_option.price * booking.num_seats
        
        if commit:
            # Update available seats
            self.travel_option.available_seats -= booking.num_seats
            self.travel_option.save()
            booking.save()
        
        return booking
