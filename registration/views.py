from django.shortcuts import render,redirect
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model,authenticate
from django.contrib import messages,auth
from django.conf import settings
from .models import Profile, Appointments, Prescription, Invoice

User = get_user_model()
def nregistration(request):
    if request.method == "POST":
        first_name=request.POST["fname"]
        last_name=request.POST["lname"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        cnfpassword=request.POST["cnfpassword"]
        profession="reception"
        if password==cnfpassword:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'User Already Exists')
                return render(request,'nregistration.html')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=cnfpassword,profession=profession,is_staff=True,is_active=True)
                user.groups.add(1)
                user.save()
                storage = messages.get_messages(request)
                storage.used = True
                messages.info(request,'Receptionist Registered Successfully')
                return redirect('/home')
        else:
            messages.warning(request,'Passwords are not matching')
            return render(request,'nregistration.html')
    else:

        return render(request, 'nregistration.html')

def registration(request):
    if request.method == "POST":
        first_name=request.POST["fname"]
        last_name=request.POST["lname"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        cnfpassword=request.POST["cnfpassword"]
        profession=request.POST["profession"]
        if password==cnfpassword:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'User Already Exists')
                return render(request,'registration.html')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=cnfpassword,profession=profession)
                user.save()
                storage = messages.get_messages(request)
                storage.used = True
                messages.info(request,'User Registered Successfully')
                return redirect('/home')
        else:
            messages.warning(request,'Passwords are not matching')
            return render(request,'registration.html')
    else:

        return render(request, 'registration.html')

def login(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'User Login Success')    
            return redirect('/home')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.warning(request,'Wrong Password')
            return render(request,'login.html')
    else:
        return render(request,'login.html')
def logout(request):
    auth.logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Logged Out Successfully')

    return redirect('/home')
def profile(request):
    if request.method=="POST":
        username=request.POST.get("username")
        profession=request.POST["profession"]
        gender=request.POST.get("gender")
        age=int(request.POST["age"])
        aptname=request.POST["aptname"]
        stname=request.POST["stname"]
        cityname=request.POST["cityname"]
        distname=request.POST["distname"]
        statename=request.POST["statename"]
        countryname=request.POST["countryname"]
        insurance=request.POST.get("insurance")
        phone=request.POST["phone"]
        medicalhistory=request.FILES.get("medicalhistory")
        bloodgroup=request.POST.get("bloodgroup")
        filename=0
        if medicalhistory is not None:
            fs = FileSystemStorage()
            filename = fs.save(medicalhistory.name,medicalhistory)
        if Profile.objects.filter(username=username).exists():
            obj=Profile.objects.filter(username=username).update(age=age,aptname=aptname,stname=stname,cityname=cityname,distname=distname,statename=statename,countryname=countryname,phone=phone)
        else:
            obj=Profile.objects.create(username=username,profession=profession,gender=gender,age=age,aptname=aptname,stname=stname,cityname=cityname,distname=distname,statename=statename,countryname=countryname,phone=phone,insurance=insurance,MedicalHistory=filename,bloodgroup=bloodgroup)
            obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Profile Updated Successfully')    
        return redirect('/home')
    else:
        obj=Profile.objects.all().filter(username=request.user.username)
        if len(obj)==0:
            return render(request,'profile1.html')
        else:
            return render(request,'profile.html',{'obj':obj[0]})
def nappointment(request):
    if request.method=="POST":
        duser=request.POST.get('duser')
        puser=request.POST.get('puser')
        date=request.POST["date"]
        time=request.POST["time"]
        status=request.POST["status"]
        disease=request.POST["disease"]
        obj=Appointments.objects.create(duser=duser,puser=puser,date=date,time=time,status=status,disease=disease)
        obj.save()
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Appointment Created Successfully')    
        return redirect('/home')

    else:
        doctor_objects=User.objects.all().filter(profession="doctor")
        patient_objects=User.objects.all().filter(profession="patient")
        return render(request,'nurseappointment.html',{'doctor_obj':doctor_objects,'patient_obj':patient_objects})
def appointment(request):
    if request.user.profession == "doctor":
        objects=Appointments.objects.all().filter(duser=request.user.username)
        return render(request,'dashboard.html',{'objects':objects})
    if request.user.profession == "patient":
        objects=Appointments.objects.all().filter(puser=request.user.username)
        return render(request,'dashboard.html',{'objects':objects})
    if request.user.profession == "reception" or request.user.is_superuser==True:
        objects=Appointments.objects.all()
        total_appointments=len(objects)
        completed_appointments=len(Appointments.objects.filter(status="Completed"))
        active_appointments=len(Appointments.objects.filter(status="Active"))
        return render(request,'dashboard.html',{'objects':objects,'ac':active_appointments,'com':completed_appointments,'tot':total_appointments})
def prescription(request):
    if request.method=="POST":
        puser=request.POST["puser"]
        disease=request.POST["disease"]
        date=request.POST["date"]
        medicine=request.POST["medicine"]
        duser=request.user.username
        care=request.POST["care"]
        amount=request.POST["amount"]
        update_id=request.POST["id"]
        obj=Prescription.objects.create(puser=puser,disease=disease,date=date,medicine=medicine,duser=duser,care=care)
        Appointments.objects.filter(puser=puser,duser=request.user.username,id=update_id).update(status="Completed")
        obj2=Invoice.objects.create(puser=puser,disease=disease,duser=duser,amount=amount,payment="NotPaid")
        obj2.save()
        obj.save()

        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Prescription Created Successfully')    
        return redirect('/home')
    else:
        patient_objects=Appointments.objects.all().filter(duser=request.user.username,status="Active")
        if len(patient_objects)>0:
            return render(request,"prescription.html",{'p_appoint':patient_objects[0]})
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'No Active Prescription')    
            return redirect('/registration/medical')    
def medical(request):
    if request.user.profession=='doctor':
        pres_objs=Prescription.objects.all().filter(duser=request.user.username)
        return render(request,'medical.html',{'pres_obj':pres_objs})
    if request.user.profession=='patient':
        pres_objs=Prescription.objects.all().filter(puser=request.user.username)
        return render(request,'medical.html',{'pres_obj':pres_objs})
    if request.user.is_superuser==True:
        pres_objs=Prescription.objects.all()
        return render(request,'medical.html',{'pres_obj':pres_objs})
def invoice(request):
    if request.user.profession=="patient":
        objects=Invoice.objects.all().filter(puser=request.user.username)
        return render(request,'invoice.html',{'objects':objects})
    if request.user.profession=="reception" or request.user.is_superuser==True:
        objects=Invoice.objects.all()
        return render(request,'invoice.html',{'objects':objects})

def analytics(request):
    obj=Invoice.objects.all()
    total_invoice=len(obj)
    obj1=Invoice.objects.all().filter(payment="Paid")
    paid_invoice=len(obj1)
    recieved_amount=0
    for item in obj1:
        recieved_amount+=item.amount
    obj1=Invoice.objects.all().filter(payment="NotPaid")
    pending_invoice=len(obj1)
    need_amount=0
    for item in obj1:
        need_amount+=item.amount
    return render(request,'analytics.html',{'objects':obj,'total_invoice':total_invoice,'pinvoice':paid_invoice,'npinvoice':pending_invoice,'ramount':recieved_amount,'pamount':need_amount,'rpamount':recieved_amount+need_amount})

def showinv(request,number):
    obj=Invoice.objects.all().filter(id=number)
    return render(request,'showinv.html',{'objects':obj})
