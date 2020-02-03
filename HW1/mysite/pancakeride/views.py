from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ride, Driver
from django.db import IntegrityError
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.core.mail import EmailMessage

from .forms import DriverRegisteForm, RideRequestForm

@login_required
def Driver_regist(request):
    if request.method == 'POST':
        form = DriverRegisteForm(request.POST)
        if form.is_valid():
            if Driver.objects.filter(user = request.user).exists():
                # have registed
                return redirect(reverse('login'))
            driver_info = Driver.objects.create(user = request.user,capacity = 1)
            driver_info.first_name = form.cleaned_data['first_name']
            driver_info.last_name = form.cleaned_data['last_name']
            driver_info.license_plate_number = form.cleaned_data['license_plate_number']
            driver_info.capacity = form.cleaned_data['capacity']
            driver_info.special_vehicle_info = form.cleaned_data['special_vehicle_info']
            driver_info.vehicle_type = form.cleaned_data['vehicle_type']
            driver_info.save()
            return redirect(reverse('login'))
    else:
        form = DriverRegisteForm()
    return render(request, 'Driver/driver_register.html', {'form': form})


def Ride_request(request):
    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride_info = Ride.objects.create(owner = request.user)
            ride_info.passenger_num = form.cleaned_data['passenger_num']
            ride_info.destination = form.cleaned_data['destination']
            ride_info.arrival_time = form.cleaned_data['arrival_time']
            ride_info.vehicle_type = form.cleaned_data['vehicle_type']
            ride_info.special_vehicle_info = form.cleaned_data['special_vehicle_info']
            ride_info.shareable = form.cleaned_data['shareable']

            ride_info.save()
            return redirect(reverse('login'))

    else:
        form = RideRequestForm()
    return render(request, 'Ride/ride_request.html', {'form': form})