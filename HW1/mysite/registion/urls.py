from django.urls import path
from django.conf.urls import url
from registion import views

urlpatterns = [
  path('register/', views.RegisterView.as_view(), name='register'),
]