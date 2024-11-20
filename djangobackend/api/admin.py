from django.contrib import admin
from .models import Student,Cruise,CruiseDetail,CruiseDetailFinal, Booking,LogedInUser
# from .models import Cruise
# Register your models here.
@admin.register(Student)

class StudentAdmin(admin.ModelAdmin):
    list_display=['id','stuname','email']

@admin.register(Cruise)

class CruiseAdmin(admin.ModelAdmin):
    list_display=['id','type','month','origin','departure','visiting','nights','decks','cost','seats','startDate','endDate','country','continent','image']


@admin.register(CruiseDetail)

class CruiseDetailAdmin(admin.ModelAdmin):
    list_display=['id','type','month','origin','departure','visiting','nights','decks','cost','seats','startDate','endDate','country','continent','image','cruiseName']


@admin.register(CruiseDetailFinal)

class CruiseDetailFinalAdmin(admin.ModelAdmin):
    list_display=['id','type','month','origin','departure','visiting','nights','decks','cost','seats','startDate','endDate','country','continent','image','cruiseName','oceanviewRooms','InteriorRooms','oceanviewForward','oceanviewMiddle','oceanviewAft','InteriorForward','InteriorMiddle','InteriorAft','oceanviewRoomsCost','InteriorRoomsCost']


# @admin.register(CruiseDetailsDone)

# class CruiseDetailsDoneAdmin(admin.ModelAdmin):
#     list_display=['id','type','month','origin','departure','visiting','nights','decks','cost','seats','startDate','endDate','country','continent','image','cruiseName','oceanviewRooms','InteriorRooms','oceanviewForward','oceanviewMiddle','oceanviewAft','InteriorForward','InteriorMiddle','InteriorAft','oceanviewRoomsCost','InteriorRoomsCost']
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('cruise', 'room_type', 'room_number','location', 'user')
    search_fields = ('user__username', 'room_number')

@admin.register(LogedInUser)
class LogedInUserAdmin(admin.ModelAdmin):
    list_display=('username','email','password')
    