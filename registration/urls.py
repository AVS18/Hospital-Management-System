from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path("register",views.registration,name="registration"),
    path("login",views.login,name="login"),
    path("profile",views.profile,name="profile"),
    path("logout",views.logout,name="logout"),
    path("nappointment",views.nappointment,name="nappointment"),
    path("appointment",views.appointment,name="appointment"),
    path("prescription",views.prescription,name="prescription"),
    path("medical",views.medical,name="medical"),
    path("invoice",views.invoice,name="invoice"),
    path("nregistration",views.nregistration,name="nregistration"),
    path("analytics",views.analytics,name="analytics"),
    path("showinv/<int:number>",views.showinv,name="showinv")
]
