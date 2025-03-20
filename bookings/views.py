from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking
from .forms import BookingForm
from travels.models import TravelOption


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def booking_create(request, travel_id):
    travel_option = get_object_or_404(TravelOption, travel_id=travel_id)
    
    if travel_option.available_seats <= 0:
        messages.error(request, 'Sorry, no seats available for this travel option.')
        return redirect('travel-list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel_option)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.travel_option = travel_option
            booking.total_price = travel_option.price * form.cleaned_data['num_seats']
            booking.save()
            
            messages.success(request, f'Booking successful! Your booking ID is {booking.booking_id}.')
            return redirect('booking-detail', booking_id=booking.booking_id)
    else:
        form = BookingForm(travel_option=travel_option)
    
    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'travel': travel_option
    })


@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if booking.status == 'Cancelled':
        messages.warning(request, 'This booking is already cancelled.')
        return redirect('booking-detail', booking_id=booking.booking_id)
    
    if request.method == 'POST':
        # Update booking status
        booking.status = 'Cancelled'
        booking.save()
        
        # Return seats to travel option
        travel_option = booking.travel_option
        travel_option.available_seats += booking.num_seats
        travel_option.save()
        
        messages.success(request, 'Your booking has been cancelled successfully.')
        return redirect('booking-list')
    
    return render(request, 'bookings/booking_cancel.html', {'booking': booking})

