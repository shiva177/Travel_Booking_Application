from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import TravelOption
from .forms import TravelFilterForm, TravelOptionForm


def travel_list(request):
    form = TravelFilterForm(request.GET)
    travels = TravelOption.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['type']:
            travels = travels.filter(type=form.cleaned_data['type'])
        if form.cleaned_data['source']:
            travels = travels.filter(source__icontains=form.cleaned_data['source'])
        if form.cleaned_data['destination']:
            travels = travels.filter(destination__icontains=form.cleaned_data['destination'])
        if form.cleaned_data['departure_date']:
            travels = travels.filter(departure_date=form.cleaned_data['departure_date'])
        if form.cleaned_data['max_price']:
            travels = travels.filter(price__lte=form.cleaned_data['max_price'])
    
    context = {
        'form': form,
        'travels': travels
    }
    return render(request, 'travels/travel_list.html', context)


def travel_detail(request, travel_id):
    travel = get_object_or_404(TravelOption, travel_id=travel_id)
    return render(request, 'travels/travel_detail.html', {'travel': travel})


@login_required
@user_passes_test(lambda u: u.is_staff)
def travel_create(request):
    if request.method == 'POST':
        form = TravelOptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Travel option created successfully!')
            return redirect('travel-list')
    else:
        form = TravelOptionForm()
    
    return render(request, 'travels/travel_form.html', {'form': form, 'title': 'Create Travel Option'})


@login_required
@user_passes_test(lambda u: u.is_staff)
def travel_update(request, travel_id):
    travel = get_object_or_404(TravelOption, travel_id=travel_id)
    
    if request.method == 'POST':
        form = TravelOptionForm(request.POST, instance=travel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Travel option updated successfully!')
            return redirect('travel-detail', travel_id=travel.travel_id)
    else:
        form = TravelOptionForm(instance=travel)
    
    return render(request, 'travels/travel_form.html', {
        'form': form,
        'title': 'Update Travel Option',
        'travel': travel
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def travel_delete(request, travel_id):
    travel = get_object_or_404(TravelOption, travel_id=travel_id)
    
    if request.method == 'POST':
        travel.delete()
        messages.success(request, 'Travel option deleted successfully!')
        return redirect('travel-list')
    
    return render(request, 'travels/travel_confirm_delete.html', {'travel': travel})

