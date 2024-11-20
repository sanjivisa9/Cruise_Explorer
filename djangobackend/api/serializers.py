# from rest_framework import serializers 
# from .models import Student
# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Student
#         fields=['id','stuname','email']


from rest_framework import serializers
from .models import Student,Cruise,CruiseDetail,CruiseDetailFinal,Booking,LogedInUser

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password 

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'stuname', 'email']


class CruiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cruise
        fields = ['id','type','month','origin','departure','visiting','nights','decks','cost','seats','startDate','endDate','country','continent','image']


class CruiseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CruiseDetail
        fields =['id','type','month','origin','departure','visiting','nights','decks','cost','seats','startDate','endDate','country','continent','image','cruiseName','oceanviewRooms','InteriorRooms','oceanviewForward','oceanviewMiddle','oceanviewAft','InteriorForward','InteriorMiddle','InteriorAft','oceanviewRoomsCost','InteriorRoomsCost']


class CruiseDetailFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CruiseDetailFinal
        fields =['id','type','month','origin','departure','visiting','nights','decks','cost','seats','startDate','endDate','country','continent','image','cruiseName','oceanviewRooms','InteriorRooms','oceanviewForward','oceanviewMiddle','oceanviewAft','InteriorForward','InteriorMiddle','InteriorAft','oceanviewRoomsCost','InteriorRoomsCost']

# class CruiseDetailsDoneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CruiseDetailsDone
#         fields = ['id','type','month','origin','departure','visiting','nights','decks','cost','seats','startDate','endDate','country','continent','image','cruiseName','oceanviewRooms','InteriorRooms','oceanviewForward','oceanviewMiddle','oceanviewAft','InteriorForward','InteriorMiddle','InteriorAft']
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['cruise', 'room_type', 'room_number','location', 'user']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LogedInUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = LogedInUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Hash the password using make_password
        user = LogedInUser(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password'])  # Use make_password here
        )
        user.save()
        return user