from django.shortcuts import render
from django.db import connection
from django.contrib import messages
def home(request):
    return render(request, 'home.html')
def about(request):
    storage = messages.get_messages(request)
    storage.used = True
    return render(request,'about.html')
def contact(request):
    storage = messages.get_messages(request)
    storage.used = True
    return render(request,'contact.html')