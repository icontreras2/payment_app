from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Scheduling, Payment
from django.contrib.auth.models import User


class SchedulingForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['customer', 'professional', 'start_datetime', 'end_datetime', 'description']

class SchedulingFormForCustomer(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = ['professional', 'start_datetime', 'end_datetime', 'description']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method', 'currency_type', 'status', 'scheduling']

class ProfessionalRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=200)
    occupation = forms.CharField(max_length=100)
    phone = forms.IntegerField()
    charge_per_minute_in_chilean_pesos = forms.FloatField()
    rut = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'occupation', 'phone', 'charge_per_minute_in_chilean_pesos', 'rut')

class CustomerRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=200)
    phone = forms.IntegerField()
    rut = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'phone', 'rut')

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')