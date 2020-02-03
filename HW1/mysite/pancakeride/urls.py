from django.urls import path
from django.views.generic.base import TemplateView 
from .import views

app_name = 'pancakeride'
urlpatterns =[
    path('driver/register/', views.Driver_regist, name='driver_register'),
    path('ride/request', views.Ride_request, name='ride_request'),
    path('ride/edit/<uuid:pk>/', views.Ride_request_edit, name='ride_request_edit'),
    path('ride/detail/<uuid:pk>/', views.Ride_request_detail, name='ride_detail'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]