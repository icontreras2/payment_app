"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from payment_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("professional/<int:professional_id>/schedulings/", views.get_schedulings_of_professional, name="get_schedulings_of_professional"),
    path("schedulings/add/", views.add_scheduling, name="add_scheduling"),
    path("add_scheduling_by_customer/<int:customer_id>", views.add_scheduling_by_customer, name="add_scheduling_by_customer"),
    path("schedulings/<int:scheduling_id>/", views.change_scheduling_paid_status, name="change_scheduling_paid_status"),
    path("schedulings/<int:scheduling_id>/add_payment", views.pay_scheduling, name="pay_scheduling"),
    path("schedulings/<int:scheduling_id>/successful_payment", views.pay_successfully, name="successful_payment"),
    path('register_professional/', views.register_professional, name='register_professional'),
    path('register_admin/', views.register_admin, name='register_admin'),
    path('register_customer/', views.register_customer, name='register_customer'),
    path('logout/', views.logout_account, name='logout'),
    path('login/', views.login_user, name='login'),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.home, name="home")
]
