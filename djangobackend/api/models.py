from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your models here.
class Student(models.Model):
    stuname=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    def __str__(self):
        return self.email
# from django.db import models

# class Student(models.Model):
#     stuname = models.CharField(max_length=100)
#     email = models.EmailField()


class Cruise(models.Model):
    type=models.CharField(max_length=100)
    month=models.CharField(max_length=100)
    origin=models.CharField(max_length=100)
    departure=models.CharField(max_length=100)
    visiting=models.CharField(max_length=1000)
    nights=models.IntegerField(default=0)
    decks=models.IntegerField(default=0)
    cost=models.IntegerField(default=0)
    seats=models.IntegerField(default=0)
    startDate=models.DateField()
    endDate=models.DateField()
    country=models.CharField(max_length=100)
    continent=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cruise/images",default="")
    # cruiseName=models.CharField(max_length=100, default="Unnamed Cruise")


    def __str__(self):
        return self.origin
    

class CruiseDetail(models.Model):
    type=models.CharField(max_length=100)
    month=models.CharField(max_length=100)
    origin=models.CharField(max_length=100)
    departure=models.CharField(max_length=100)
    visiting=models.CharField(max_length=1000)
    nights=models.IntegerField(default=0)
    decks=models.IntegerField(default=0)
    cost=models.IntegerField(default=0)
    seats=models.IntegerField(default=0)
    startDate=models.DateField()
    endDate=models.DateField()
    country=models.CharField(max_length=100)
    continent=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cruise/images",default="")
    cruiseName=models.CharField(max_length=100, default="Unnamed Cruise")


    def __str__(self):
        return self.origin
    
class CruiseDetailFinal(models.Model):
    type=models.CharField(max_length=100)
    month=models.CharField(max_length=100)
    origin=models.CharField(max_length=100)
    departure=models.CharField(max_length=100)
    visiting=models.CharField(max_length=1000)
    nights=models.IntegerField(default=0)
    decks=models.IntegerField(default=0)
    cost=models.IntegerField(default=0)
    seats=models.IntegerField(default=0)
    startDate=models.DateField()
    endDate=models.DateField()
    country=models.CharField(max_length=100)
    continent=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cruise/images",default="")
    cruiseName=models.CharField(max_length=100, default="Unnamed Cruise")
    oceanviewRooms=models.IntegerField(default=0)
    InteriorRooms=models.IntegerField(default=0)
    oceanviewForward=models.IntegerField(default=0)
    oceanviewMiddle=models.IntegerField(default=0)
    oceanviewAft=models.IntegerField(default=0)
    InteriorForward=models.IntegerField(default=0)
    InteriorMiddle=models.IntegerField(default=0)
    InteriorAft=models.IntegerField(default=0)
    oceanviewRoomsCost=models.IntegerField(default=0)
    InteriorRoomsCost=models.IntegerField(default=0)



    def __str__(self):
        return self.cruiseName

# class CruiseDetailsDone(models.Model):
#     type=models.CharField(max_length=100)
#     month=models.CharField(max_length=100)
#     origin=models.CharField(max_length=100)
#     departure=models.CharField(max_length=100)
#     visiting=models.CharField(max_length=1000)
#     nights=models.IntegerField(default=0)
#     decks=models.IntegerField(default=0)
#     cost=models.IntegerField(default=0)
#     seats=models.IntegerField(default=0)
#     startDate=models.DateField()
#     endDate=models.DateField()
#     country=models.CharField(max_length=100)
#     continent=models.CharField(max_length=100)
#     image=models.ImageField(upload_to="cruise/images",default="")
#     cruiseName=models.CharField(max_length=100, default="Unnamed Cruise")
#     oceanviewRooms=models.IntegerField(default=0)
#     InteriorRooms=models.IntegerField(default=0)
#     oceanviewForward=models.IntegerField(default=0)
#     oceanviewMiddle=models.IntegerField(default=0)
#     oceanviewAft=models.IntegerField(default=0)
#     InteriorForward=models.IntegerField(default=0)
#     InteriorMiddle=models.IntegerField(default=0)
#     InteriorAft=models.IntegerField(default=0)
#     oceanviewRoomsCost=models.IntegerField(default=0)
#     InteriorRoomsCost=models.IntegerField(default=0)



#     def __str__(self):
#         return self.cruiseName


class Booking(models.Model):
    cruise = models.ForeignKey(CruiseDetailFinal, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)
    location = models.CharField(max_length=500,default='')  
    user = models.EmailField(default='')

    def __str__(self):
        return f"{self.user} - {self.room_type} {self.room_number}"


class LogedInUser(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(default="")
    password=models.CharField(max_length=100)
