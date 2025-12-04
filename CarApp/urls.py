from django.urls import path
from .views import *

urlpatterns = [
     path("", home, name="home"),
     path("create_staff/", create_staff, name="create-staff"),
     path("login_staff/", login_staff, name="login-staff"),
     path("logout-staff/", logout_staff, name="logout-staff"),
     path("add_car/", add_car, name="add-car" ),
     path('register_customer/',  register_customer, name="register-customer"),
     path("sell_car/", sell_car, name="sell-car"),
     path("dashboard/", dashboard, name="dashboard"),
     path("service", service, name="service")
]
