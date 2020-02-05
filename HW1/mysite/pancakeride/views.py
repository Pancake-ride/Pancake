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

from .forms import DriverRegisteForm, RideRequestForm, SharerSearchForm

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

@login_required
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

@login_required
def Ride_request_edit(request, pk):
    ride_edit = get_object_or_404(Ride, pk = pk)
    if ride_edit.owner != request.user:
        print('ride request edit id error')
    if ride_edit.status != 'op':
        print('Only open ride can be edited!')
        return redirect(reverse('login'))
    if request.method == 'POST':
        edit_form = RideRequestForm(request.POST)
        if edit_form.is_valid():
            ride_edit.passenger_num = edit_form.cleaned_data['passenger_num']
            ride_edit.destination = edit_form.cleaned_data['destination']
            ride_edit.arrival_time = edit_form.cleaned_data['arrival_time']
            ride_edit.vehicle_type = edit_form.cleaned_data['vehicle_type']
            ride_edit.special_vehicle_info = edit_form.cleaned_data['special_vehicle_info']
            ride_edit.shareable = edit_form.cleaned_data['shareable']
            ride_edit.save()
            return redirect(reverse('login'))
    else:
        print(ride_edit.destination)
        form = RideRequestForm(initial = {
            'passenger_num': ride_edit.passenger_num,
            'destination': ride_edit.destination,
            'arrival_time': ride_edit.arrival_time,
            'vehicle_type': ride_edit.vehicle_type,
            'special_vehicle_info': ride_edit.special_vehicle_info,
            'shareable': ride_edit.shareable,
        })

        context = {
            'form': form,
            'ride_edit': ride_edit,
        }
        return render(request, 'Ride/ride_request_edit.html', context)

@login_required
def Ride_request_detail(request, pk):
    ride_detail = get_object_or_404(Ride, pk = pk)
    if ride_detail.owner != request.user:
        print('user Id error!')
    context = {'ride_detail': ride_detail}
    return render(request, 'Ride/ride_detail.html', context)

class RideListView(LoginRequiredMixin, generic.ListView):
    model = Ride
    template_name = 'Ride/ride_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        status = self.request.GET.get('s')
        context = super().get_context_data(**kwargs)
        context['owner_ride_list'] = Ride.objects.filter(owner__exact=self.request.user).filter(status__exact=status)
        context['sharer_ride_list'] = Ride.objects.filter(sharer=self.request.user).filter(status__exact=status)
        context['driver_ride_list'] = Ride.objects.filter(driver__user=self.request.user).filter(status__exact=status)
        return context

def Sharer_search(request):
    context = {}
    if request.POST:
        form = SharerSearchForm(request.POST)
        if form.is_valid():
            destination = form.cleaned_data['destination']
            early_arrival_time = form.cleaned_data['early_arrival_time']
            late_arrival_time = form.cleaned_data['late_arrival_time']
            sharer_num = form.cleaned_data['sharer_num']

            
            
            available_rides = Ride.objects.filter(destination__exact = destination).filter(arrival_time__gte = early_arrival_time).filter(arrival_time__lte = late_arrival_time).filter(status__exact = 'op')#.filter(shareable__exact = )
            context['form'] = form
            context['availabel_rides'] = available_rides
            return render(request, 'Sharer/sharer_search.html', context)
        else:
            print('invalid form')

    else:
        form = SharerSearchForm()
        context = {'form': form}
        return render(request, 'Sharer/sharer_search.html', context)


def Sharer_confirm(request, pk):
    if request.POST:
        print('ppost')
    else:
        print('gget')
        print(pk)