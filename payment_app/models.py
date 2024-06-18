from django.db import models
from django.core.exceptions import ValidationError
from .constants import (
    PAYMENT_STATUS, 
    SCHEDULING_STATUS,
    PAYMENT_METHODS,
    CURRENCY_TYPES,
    PROFESSIONAL_OCCUPATIONS,
)
from django.contrib.auth.models import User


class Professional(models.Model):
    def __str__(self):
        return self.name

    @property
    def get_occupation(self):
        for occupation in PROFESSIONAL_OCCUPATIONS:
            if self.occupation == occupation[0]:
                return occupation[1]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=200)
    occupation = models.CharField(max_length=100, choices=PROFESSIONAL_OCCUPATIONS, null=True, blank=True)
    phone = models.IntegerField(blank=True)
    charge_per_minute_in_chilean_pesos = models.FloatField(blank=True)
    rut = models.CharField(blank=True, max_length=20)

class Customer(models.Model):
    def __str__(self):
        return self.name

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=200)
    phone = models.IntegerField(blank=True)
    rut = models.CharField(blank=True, max_length=20)

class Scheduling(models.Model):
    @property
    def customer_and_professional_information(self):
        return f"cliente {self.customer.name} con profesional {self.professional.name}"
    
    @property
    def datetime_information(self):
        start_datetime = self.start_datetime.strftime("%d/%m/%Y (%H:%M)")
        end_datetime = self.end_datetime.strftime("%d/%m/%Y (%H:%M)")
        return f"desde {start_datetime} hasta {end_datetime}"
    
    @property
    def information(self):
        return self.customer_and_professional_information + " " + self.datetime_information
    
    def __str__(self):
        return "Agendamiento de " + self.customer_and_professional_information
    
    @property
    def get_status(self):
        if self.status == "paid":
            return "Pagado"
        else:
            return "No pagado"

    def clean(self):
        if self.start_datetime.date() != self.end_datetime.date():
            raise ValidationError('Las fechas deben ser del mismo día.')

        if self.start_datetime >= self.end_datetime:
            raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=SCHEDULING_STATUS, null=True, blank=True, default="unpaid")

class Payment(models.Model):
    @property
    def scheduling_information(self):
        return "Agendamiento de " + self.scheduling.information
    
    def __str__(self):       
        return f"Pago asociado a agendamiento de {self.scheduling.information}"

    scheduling = models.ForeignKey(Scheduling, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, null=True, blank=True)
    method = models.CharField(max_length=30, choices=PAYMENT_METHODS, blank=True)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPES)
    amount = models.FloatField()