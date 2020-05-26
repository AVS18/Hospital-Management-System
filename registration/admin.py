from django.contrib import admin
from .models import User
from .models import Profile
from .models import Appointments
from .models import Prescription
from .models import Invoice

class Customize_userreges(admin.ModelAdmin):
    list_display=['first_name','last_name','username','email','profession']
    list_filter=(['profession'])
class Customize_Profile(admin.ModelAdmin):

    list_display=['username','gender','age','aptname','stname','cityname','phone','profession','MedicalHistory']
    list_filter=(['profession','insurance'])

class Customize_Appointments(admin.ModelAdmin):
    list_display=['duser','date','puser','time','status','disease']
    list_filter=(['duser','puser','disease'])

class Customize_Prescription(admin.ModelAdmin):
    list_display=['duser','disease','puser','date','care','medicine']
    list_filter=(['disease','medicine'])

class Customize_Invoice(admin.ModelAdmin):
    list_display=['puser','duser','amount','disease','payment']
    list_filter=(['puser','duser','disease','payment'])

admin.site.register(User,Customize_userreges)
admin.site.register(Profile,Customize_Profile)
admin.site.register(Appointments,Customize_Appointments)
admin.site.register(Prescription,Customize_Prescription)
admin.site.register(Invoice,Customize_Invoice)