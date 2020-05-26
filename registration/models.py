from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profession=models.CharField(max_length=100,blank=True)

class Profile(models.Model):
    username=models.CharField(max_length=100,blank=True)
    profession=models.CharField(max_length=100,blank=True)
    gender=models.CharField(max_length=6,blank=True)
    age=models.BigIntegerField(blank=True)
    aptname=models.CharField(max_length=60,blank=True)
    stname=models.CharField(max_length=60,blank=True)
    cityname=models.CharField(max_length=60,blank=True)
    distname=models.CharField(max_length=60,blank=True)
    statename=models.CharField(max_length=60,blank=True)    
    countryname=models.CharField(max_length=60,blank=True)
    phone=models.CharField(max_length=12,blank=True)
    insurance=models.CharField(max_length=60,blank=True)
    MedicalHistory=models.FileField(upload_to='medical history')
    bloodgroup=models.CharField(max_length=20,blank=True)

class Appointments(models.Model):
    duser=models.CharField(max_length=60,blank=True)
    puser=models.CharField(max_length=60,blank=True)
    date=models.CharField(max_length=15,blank=True)
    time=models.CharField(max_length=15,blank=True)
    status=models.CharField(max_length=15,blank=True)
    disease=models.CharField(max_length=200,blank=True)

class Prescription(models.Model):
    puser=models.CharField(max_length=60,blank=True)
    disease=models.CharField(max_length=200,blank=True)
    date=models.CharField(max_length=15,blank=True)
    medicine=models.CharField(max_length=60,blank=True)
    duser=models.CharField(max_length=60,blank=True)
    care=models.CharField(max_length=60,blank=True)

class Invoice(models.Model):
    puser=models.CharField(max_length=60,blank=True)
    duser=models.CharField(max_length=60,blank=True)
    amount=models.BigIntegerField(blank=True)
    disease=models.CharField(max_length=60,blank=True)
    payment=models.CharField(max_length=60,blank=True)