from django.urls import path
from . import views

urlpatterns = [
    path('',views.qr_form,name='qr_form'),
]