from django.forms import ModelForm
#from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Driver, Ride
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class DriverRegisteForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 
                  'license_plate_number', 'capacity',
                  'special_vehicle_info', 'vehicle_type']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'license_plate_number': 'Plate number',
            'capacity': 'Capacity',
            'special_vehicle_info': 'Special_vehicle_info',
            'vehicle_type': 'Vehicle type'
        }

class RideRequestForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['passenger_num', 'destination',
                  'arrival_time', 'vehicle_type',
                  'special_vehicle_info', 'shareable']
        labels = {
            'passenger_num' : 'Number of passengers',
            'destination': 'Your destination',
            'arrival_time': 'Anticipate arrival time',
            'vehicle_type': 'Vechicle type',
            'special_vehicle_info': 'Special vehicle require',
            'shareable': 'Will you allow share ride'
        }