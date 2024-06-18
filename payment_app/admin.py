from django.contrib import admin
from .models import Payment, Professional, Customer, Scheduling


class ProfessionalAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "occupation", 
        "rut", 
        "phone", 
        "charge_per_minute_in_chilean_pesos"
    )
    search_fields = (
        "name",
        "phone"
    )
    list_filter = ("occupation",)

class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "rut",
        "phone"
    )
    search_fields = (
        "name", 
        "phone"
    )

class SchedulingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_datetime",
        "end_datetime",
        "customer",
        "professional",
        "status",
    )
    list_filter = ("status",)

class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "amount",
        "currency_type",
        "status", 
        "method",
        "scheduling_information",
        "datetime",
    )
    list_filter = (
        "status", 
        "method"
    )

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Professional, ProfessionalAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Scheduling, SchedulingAdmin)