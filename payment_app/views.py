from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from .models import Scheduling, Professional, Customer
from datetime import datetime
from django.contrib import messages
from .forms import (
    SchedulingForm, 
    PaymentForm, 
    ProfessionalRegistrationForm, 
    CustomerRegistrationForm, 
    AdminRegistrationForm, 
    SchedulingFormForCustomer
)
from .constants import (
    PROFESSIONAL_OCCUPATIONS, 
    CURRENCY_INFO, 
    PAYMENT_METHODS
)
from .get_payment_status import get_payment_status


def home(request):
    professionals = Professional.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request, 'payment_app/logged_admin_home.html', {'professionals': professionals})
        try:
            professional = Professional.objects.get(user=request.user)
            schedulings_query_set = Scheduling.objects.filter(professional=professional)
            schedulings = []
            for scheduling in schedulings_query_set:
                scheduling_info = {
                    "id": scheduling.id,
                    "customer_name": scheduling.customer.name,
                    "professional_name": scheduling.professional.name,
                    "professional_occupation": scheduling.professional.get_occupation,
                    "start_datetime": scheduling.start_datetime,
                    "end_datetime": scheduling.end_datetime,
                    "description": scheduling.description,
                    "status": scheduling.get_status,
                }
                schedulings.append(scheduling_info)
            return render (request, 'payment_app/logged_professional_home.html', {'schedulings': schedulings})
        except Exception as exception:
            pass
        try:
            customer = Customer.objects.get(user=request.user)
            schedulings_query_set = Scheduling.objects.filter(customer=customer)
            schedulings = []
            for scheduling in schedulings_query_set:
                scheduling_info = {
                    "id": scheduling.id,
                    "customer_name": scheduling.customer.name,
                    "professional_name": scheduling.professional.name,
                    "professional_occupation": scheduling.professional.get_occupation,
                    "start_datetime": scheduling.start_datetime,
                    "end_datetime": scheduling.end_datetime,
                    "description": scheduling.description,
                    "status": scheduling.get_status,
                }
                schedulings.append(scheduling_info)
            return render (request, 'payment_app/logged_customer_home.html', {'schedulings': schedulings, 'customer': customer})
        except Exception as exception:
            return generate_response(f"An error ocurred: {exception}", is_error=True, status=400)
    else:
        return render(request, 'payment_app/unlogged_user_home.html', {'professionals': professionals})
    
def generate_response(message, is_error, status):
    if is_error:
        response = JsonResponse({"Error": message}, status=status)
    else:
        response = JsonResponse({"message": message}, status=status)
        response["Access-Control-Allow-Origin"] = "*" 
    return response

def get_schedulings_of_professional(request, professional_id):
    if request.method == "GET":
        professional = Professional.objects.get(id=professional_id)
        schedulings = Scheduling.objects.filter(professional=professional)
    else:
        return generate_response("Invalid request method", is_error=True, status=405)

    data_to_return = {
        "professional_info": {
            "id": professional.user.id,
            "name": professional.name,
            "occupation": professional.occupation,
            "phone": professional.phone,
            "email": professional.user.email,
            "rut": professional.rut,
            "charge_per_minute_in_chilean_pesos": professional.charge_per_minute_in_chilean_pesos
        },
        "schedulings": [

        ],
        "message" : "List of scheduling associated to professional successfully obtained"
    }
    for scheduling in schedulings:
        scheduling_info = {
            "id": scheduling.id,
            "customer_name": scheduling.customer.name,
            "professional_name": scheduling.professional.name,
            "start_datetime": scheduling.start_datetime,
            "end_datetime": scheduling.end_datetime,
            "description": scheduling.description,
            "status": scheduling.get_status,
        }
        data_to_return["schedulings"].append(scheduling_info)
    return render(request, 'payment_app/get_schedulings_of_professional.html', {'schedulings': data_to_return})

def add_scheduling(request):
    if request.method == 'POST':
        form = SchedulingForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                id_professional = form.cleaned_data["professional"].id
                return redirect(f'/professional/{id_professional}/schedulings/')
            return generate_response(f"Paymemnt could not be registered successfully: {form.errors}", is_error=True, status=400)
        except Exception as exception:
            return generate_response(f"Scheduling could not be registered successfully: {exception}", is_error=True, status=400)
    else:
        customers = Customer.objects.all()
        professionals = Professional.objects.all()
        form = SchedulingForm()
        return render(request, 'payment_app/add_scheduling.html', {'form': form, 'customers': customers, 'professionals': professionals})
    
def add_scheduling_by_customer(request, customer_id):
    if request.method == 'POST':
        form = SchedulingFormForCustomer(request.POST)
        try:
            if form.is_valid():
                scheduling = form.save(commit=False)
                customer = Customer.objects.get(id=customer_id)
                scheduling.customer = customer
                scheduling.save() 
                return redirect('/')
            return generate_response(f"Paymemnt could not be registered successfully: {form.errors}", is_error=True, status=400)
        except Exception as exception:
            return generate_response(f"Scheduling could not be registered successfully: {exception}", is_error=True, status=400)
    else:
        customer = Customer.objects.get(id=customer_id)
        professionals = Professional.objects.all()
        form = SchedulingFormForCustomer()
        return render(request, 'payment_app/add_scheduling_by_customer.html', {'form': form, 'customer': customer, 'professionals': professionals})

@csrf_exempt
def change_scheduling_paid_status(request, scheduling_id):
    if request.method != "PATCH":
        return generate_response("Invalid request method", is_error=True, status=405)
    try:
        scheduling = Scheduling.objects.get(id=scheduling_id)
    except Scheduling.DoesNotExist:
        return generate_response("The provided id is not from a registered scheduling.", is_error=True, status=404)
    try:
        if scheduling.status != "paid":
            scheduling.status = "paid"
        elif scheduling.status == "paid":
            scheduling.status = "unpaid"
        scheduling.save()
        return generate_response("Scheduling could be marked as paid successfully", is_error=False, status=200)
    except Exception as exception:
        return generate_response(f"Scheduling could be marked as paid: {exception}", is_error=False, status=400)

def pay_scheduling(request, scheduling_id):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        try:
            if form.is_valid():
                payment = form.save(commit=False)
                status = get_payment_status()
                payment.status = status          
                payment.datetime = datetime.utcnow()
                scheduling = Scheduling.objects.get(id=scheduling_id)
                professional = scheduling.professional
                professional_cost_per_minute_in_chilean_pesos = professional.charge_per_minute_in_chilean_pesos
                minutes_of_scheduling = (scheduling.end_datetime - scheduling.start_datetime).total_seconds() / 60
                payment_amount = CURRENCY_INFO[payment.currency_type]["equivalent_value_of_the_currency_to_one_chilean_peso"]*professional_cost_per_minute_in_chilean_pesos*minutes_of_scheduling
                payment.amount = payment_amount
                payment.save()
                if payment.status == "successful":
                    scheduling.status = "paid"
                    scheduling.save()
                    return render(request, 'payment_app/successful_payment.html', {"scheduling_id" : scheduling_id})
                else:
                    return render(request, 'payment_app/rejected_payment.html', {"scheduling_id" : scheduling_id})
            return generate_response(f"Payment was rejected: {form.errors}", is_error=True, status=400)
        except Exception as exception:
            return generate_response(f"Payment was rejected: {exception}", is_error=True, status=400)
    else:
        scheduling = Scheduling.objects.get(id=scheduling_id)
        professional = scheduling.professional
        professional_cost_per_minute_in_chilean_pesos = professional.charge_per_minute_in_chilean_pesos
        minutes_of_scheduling = (scheduling.end_datetime - scheduling.start_datetime).total_seconds() / 60
        payment_info = []
        for currency, currency_info in CURRENCY_INFO.items():
            currency_type_value = currency
            currency_type_in_spanish = currency_info["to_spanish"]
            payment_amount = str(round(professional_cost_per_minute_in_chilean_pesos*currency_info["equivalent_value_of_the_currency_to_one_chilean_peso"]*minutes_of_scheduling, 2))
            payment_info.append((currency_type_value, currency_type_in_spanish, payment_amount))
        form = PaymentForm()
        return render(request, 'payment_app/pay_scheduling.html', {'form': form, 'scheduling': scheduling, 'payment_methods': PAYMENT_METHODS, 'payment_info': payment_info})
    
def pay_successfully(request, scheduling_id):
    if request.method != "GET":
        return generate_response("Invalid request method", is_error=True, status=405)
    return render(request, 'payment_app/successful_payment.html', {'scheduling_id' : scheduling_id})

def register_professional(request):
    if request.method == 'POST':
        form = ProfessionalRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            Professional.objects.create(
                user=user, 
                name=form.cleaned_data['name'], 
                occupation=form.cleaned_data['occupation'], 
                phone=form.cleaned_data['phone'], 
                charge_per_minute_in_chilean_pesos=form.cleaned_data['charge_per_minute_in_chilean_pesos'], 
                rut=form.cleaned_data['rut']
            )
            login(request, user)
            return redirect('/') 
        else:
            return generate_response(f"Register was rejected: {form.errors}", is_error=True, status=400)
    else:
        form = ProfessionalRegistrationForm()
    return render(request, 'payment_app/register_professional.html', {'form': form, 'occupations': PROFESSIONAL_OCCUPATIONS})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            customer = Customer.objects.create(
                user=user, 
                name=form.cleaned_data['name'], 
                phone=form.cleaned_data['phone'], 
                rut=form.cleaned_data['rut']
            )
            login(request, user)
            return redirect('/') 
        else:
            return generate_response(f"El registro fue rechazado puesto que el formulario no es válido: {form.errors}", is_error=True, status=400)
    else:
        form = CustomerRegistrationForm()
    return render(request, 'payment_app/register_customer.html', {'form': form})

def logout_account(request):
    logout(request)
    return redirect('/')

def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.is_staff = True
            user.is_superuser = True
            user.save()
            login(request, user)
            return redirect('/') 
        else:
            return generate_response(f"El registro fue rechazado puesto que el formulario no es válido: {form.errors}", is_error=True, status=400)
    else:
        form = AdminRegistrationForm()
    return render(request, 'payment_app/register_admin.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')
            return redirect('/') 
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    return render(request, 'payment_app/login.html')