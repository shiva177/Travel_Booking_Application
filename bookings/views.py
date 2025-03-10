from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import TravelOption, Booking
from .forms import UserRegistrationForm, UserUpdateForm, TravelSearchForm, BookingForm

def home(request):
    # Get a few upcoming travel options for display on the homepage
    upcoming_travel = TravelOption.objects.filter(
        departure_time__gt=timezone.now()
    ).order_by('departure_time')[:5]
    
    return render(request, 'travel/home.html', {'upcoming_travel': upcoming_travel})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

def travel_list(request):
    form = TravelSearchForm(request.GET)
    travels = TravelOption.objects.filter(
        departure_time__gt=timezone.now()
    ).order_by('departure_time')
    
    # Apply filters if provided
    if form.is_valid():
        data = form.cleaned_data
        
        if data.get('travel_type'):
            travels = travels.filter(travel_type=data['travel_type'])
        
        if data.get('source'):
            travels = travels.filter(source__icontains=data['source'])
        
        if data.get('destination'):
            travels = travels.filter(destination__icontains=data['destination'])
        
        if data.get('date'):
            # Filter by date (ignoring the time part)
            date = data['date']
            travels = travels.filter(
                departure_time__year=date.year,
                departure_time__month=date.month,
                departure_time__day=date.day
            )
    
    return render(request, 'travel/travel_list.html', {
        'form': form,
        'travels': travels
    })

def travel_detail(request, travel_id):
    travel = get_object_or_404(TravelOption, pk=travel_id)
    return render(request, 'travel/travel_detail.html', {'travel': travel})

@login_required
def book_travel(request, travel_id):
    travel_option = get_object_or_404(TravelOption, pk=travel_id)
    
    # Check if there are available seats
    if travel_option.available_seats <= 0:
        messages.error(request, 'No seats available for this travel option.')
        return redirect('travel_detail', travel_id=travel_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel_option, user=request.user)
        if form.is_valid():
            booking = form.save()
            messages.success(request, f'Booking confirmed! Your booking ID is: {booking.booking_id}')
            return redirect('booking_list')
    else:
        form = BookingForm(travel_option=travel_option, user=request.user)
    
    return render(request, 'travel/booking_form.html', {
        'form': form,
        'travel': travel_option
    })

@login_required
def booking_list(request):
    active_bookings = Booking.objects.filter(user=request.user, status='confirmed')
    past_bookings = Booking.objects.filter(user=request.user, booking_date__lt=timezone.now(), status='confirmed')
    cancelled_bookings = Booking.objects.filter(user=request.user, status='cancelled')

    return render(request, 'bookings/booking_list.html', {
        'active_bookings': active_bookings,
        'past_bookings': past_bookings,
        'cancelled_bookings': cancelled_bookings
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='confirmed')
    booking.cancel_booking()
    booking.save()
    messages.success(request, "Your booking has been cancelled successfully.")
    return redirect('booking_list')