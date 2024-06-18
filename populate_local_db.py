import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
from random import choice
from payment_app.models import Payment, Professional, Customer, Scheduling


PROFESSIONALS = [
    {
        "name": "José Luis Contreras",
        "occupation": "family_doctor",
        "email": "josecontreras@gmail.com",
        "phone": 56999916619,
        "charge_per_minute_in_chilean_pesos": 1500,
        "username": "joseluis",
        "password": "contraseña123",
        "first_name": "José Luis",
        "last_name": "Contreras",
        "rut": "9497777-k",
    },
    {
        "name": "Catalina Contreras Morgado",
        "occupation": "family_doctor",
        "email": "catacontreras@gmail.com",
        "phone": 56988816619,
        "charge_per_minute_in_chilean_pesos": 2000,
        "username": "catalina",
        "password": "contraseña123",
        "first_name": "Catalina",
        "last_name": "Contreras Morgado",
        "rut": "19345687-1",
    },
    {
        "name": "Amanda Contreras Morgado",
        "occupation": "family_doctor",
        "email": "amandacontre@gmail.com",
        "phone": 56982328326,
        "charge_per_minute_in_chilean_pesos": 3000,
        "username": "amanda",
        "password": "contraseña123",
        "first_name": "Amanda",
        "last_name": "Contreras Morgado",
        "rut": "20334678-4",
    },
    {
        "name": "Jorge García",
        "occupation": "pediatrician",
        "email": "jgarcia@gmail.com",
        "phone": 56982328316,
        "charge_per_minute_in_chilean_pesos": 4000,
        "username": "jorge",
        "password": "contraseña123",
        "first_name": "Jorge",
        "last_name": "García",
        "rut": "19893627-1",
    },
    {
        "name": "Cecilia Peña",
        "occupation": "geriatrician",
        "email": "cpe@gmail.com",
        "phone": 56982328306,
        "charge_per_minute_in_chilean_pesos": 2500,
        "username": "cecilia",
        "password": "contraseña123",
        "first_name": "Cecilia",
        "last_name": "Peña",
        "rut": "20893687-1",
    },
    {
        "name": "Clemente García",
        "occupation": "lawyer",
        "email": "clemente@gmail.com",
        "phone": 56982328366,
        "charge_per_minute_in_chilean_pesos": 1500,
        "username": "clemente",
        "password": "contraseña123",
        "first_name": "Clemente",
        "last_name": "García",
        "rut": "19765633-1",
    }
]

def create_professionals():
    for professional_info in PROFESSIONALS:
        user = User.objects.create(
            username=professional_info["username"],
            email = professional_info["email"],
            first_name = professional_info["first_name"],
            last_name = professional_info["last_name"],
            is_staff = False,
            is_superuser = False,
            is_active = True,
        )
        user.set_password(professional_info["password"])
        user.save()
        professional = Professional.objects.create(
            user = user,
            name = professional_info["name"],
            occupation = professional_info["occupation"],
            phone = professional_info["phone"],
            rut = professional_info["rut"],
            charge_per_minute_in_chilean_pesos = professional_info["charge_per_minute_in_chilean_pesos"],
        )

CUSTOMERS = [
    {
        "name": "Ismael Contreras Morgado",
        "phone": 56982328336,
        "email": "ismaldinho@gmail.com",
        "rut": "19893687-1",
        "username": "ismaelcontreras",
        "password": "contraseña123",
        "first_name": "Ismael",
        "last_name": "Contreras Morgado"
    },
    {
        "name": "María Isabel De La Paz Morgado Allende",
        "phone": 56984191631,
        "email": "mariamorgado@gmail.com",
        "rut": "9407777-k",
        "username": "mariaisabel",
        "password": "contraseña123",
        "first_name": "María Isabel",
        "last_name": "Morgado Allende"
    },
    {
        "name": "Ronald López",
        "phone": 56954345645,
        "email": "ronald@gmail.com",
        "rut": "9406666-k",
        "username": "ronaldddd",
        "password": "contraseña123",
        "first_name": "Ronald",
        "last_name": "López"
    },
    {
        "name": "Fabián Vidal",
        "phone": 56983474534,
        "email": "fab@gmail.com",
        "rut": "19406666-k",
        "username": "fabito",
        "password": "contraseña123",
        "first_name": "Fabián",
        "last_name": "Vidal"
    }
]

def create_customers():
    for customer_info in CUSTOMERS:
        user = User.objects.create(
            username=customer_info['username'],
            email=customer_info['email'],
            first_name = customer_info["first_name"],
            last_name = customer_info["last_name"],
            is_staff = False,
            is_superuser = False,
            is_active = True,     
        )
        user.set_password(customer_info["password"])
        user.save()
        customer = Customer.objects.create(
            user = user,
            name = customer_info["name"],
            phone = customer_info["phone"],
            rut = customer_info["rut"],
        )


SCHEDULINGS = [
    {
        "start_datetime": datetime.strptime("2024-06-10 14:30:00", '%Y-%m-%d %H:%M:%S'),
        "end_datetime": datetime.strptime("2024-06-10 14:45:00", '%Y-%m-%d %H:%M:%S'),
        "description": "Consulta médica para dignosticar y evaluar dolor muscular.",
        "status": "unpaid"
    },
    {
        "start_datetime": datetime.strptime("2024-06-11 14:30:00", '%Y-%m-%d %H:%M:%S'),
        "end_datetime": datetime.strptime("2024-06-11 14:45:00", '%Y-%m-%d %H:%M:%S'),
        "description": "Consulta médica para dignosticar y evaluar dolor de cabeza y vómitos.",
        "status": "unpaid"
    },
    {
        "start_datetime": datetime.strptime("2024-06-12 14:30:00", '%Y-%m-%d %H:%M:%S'),
        "end_datetime": datetime.strptime("2024-06-12 14:45:00", '%Y-%m-%d %H:%M:%S'),
        "description": "Consulta médica para evaluar posible apendicitis.",
        "status": "unpaid"
    },
    {
        "start_datetime": datetime.strptime("2024-06-10 14:40:00", '%Y-%m-%d %H:%M:%S'),
        "end_datetime": datetime.strptime("2024-06-10 15:00:00", '%Y-%m-%d %H:%M:%S'),
        "description": "Consulta médica para evaluar posible COVID.",
        "status": "unpaid"
    },
    {
        "start_datetime": datetime.strptime("2024-06-12 16:30:00", '%Y-%m-%d %H:%M:%S'),
        "end_datetime": datetime.strptime("2024-06-12 16:45:00", '%Y-%m-%d %H:%M:%S'),
        "description": "Consulta médica para diagnosticar dolores de la garganta.",
        "status": "unpaid"
    }
]

def create_schedulings():
    all_professionals = Professional.objects.all()
    all_customers = Customer.objects.all()
    for scheduling_info in SCHEDULINGS:
        scheduling = Scheduling.objects.create(
            start_datetime = scheduling_info["start_datetime"],
            end_datetime = scheduling_info["end_datetime"],
            description = scheduling_info["description"],
            status = scheduling_info["status"],
            professional = choice(all_professionals),
            customer = choice(all_customers)
        )

PAYMENTS = [
    {
        "datetime": datetime.strptime("2024-06-16 12:30:00", '%Y-%m-%d %H:%M:%S'),
        "status": "successful",
        "method": "credit",
        "currency_type": "chilean-peso",
        "amount": 20000
    },
    {
        "datetime": datetime.strptime("2024-06-15 12:30:00", '%Y-%m-%d %H:%M:%S'),
        "status": "successful",
        "method": "debit",
        "currency_type": "us-dolar",
        "amount": 40
    }
]

def create_payments():
    all_schedulings = Scheduling.objects.all()
    for payment_info in PAYMENTS:
        payment = Payment.objects.create(
            datetime = payment_info["datetime"],
            status = payment_info["status"],
            method = payment_info["method"],
            scheduling = choice(all_schedulings),
            amount = payment_info["amount"],
            currency_type = payment_info["currency_type"]
        )
        if payment.status == "successful":
            payment.scheduling.status = "paid"
            payment.scheduling.save()

def populate_local_database():
    with transaction.atomic():
        create_professionals()
        create_customers()
        create_schedulings()
        create_payments()

if __name__ == "__main__":
    populate_local_database()