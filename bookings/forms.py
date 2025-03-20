from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['num_seats']
        widgets = {
            'num_seats': forms.NumberInput(attrs={'class': 'form-control seat-selector', 'min': 1, 'max': 10})
        }
    
    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        super().__init__(*args, **kwargs)
        
        if self.travel_option:
            self.fields['num_seats'].widget.attrs.update({
                'max': self.travel_option.available_seats,
                'data-price': self.travel_option.price
            })
    
    def clean_num_seats(self):
        num_seats = self.cleaned_data.get('num_seats')
        if self.travel_option and num_seats > self.travel_option.available_seats:
            raise forms.ValidationError(f"Only {self.travel_option.available_seats} seats available.")
        return num_seats

