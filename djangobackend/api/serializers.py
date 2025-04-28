from rest_framework import serializers
from .models import Student, Cruise, CruiseDetail, CruiseDetailFinal, Booking, LogedInUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'stuname', 'email']


class CruiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cruise
        fields = ['id', 'type', 'month', 'origin', 'departure', 'visiting', 'nights', 'decks', 'cost', 'seats', 'startDate', 'endDate', 'country', 'continent', 'image']


class CruiseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CruiseDetail
        fields = ['id', 'type', 'month', 'origin', 'departure', 'visiting', 'nights', 'decks', 'cost', 'seats', 'startDate', 'endDate', 'country', 'continent', 'image', 'cruiseName', 'oceanviewRooms', 'InteriorRooms', 'oceanviewForward', 'oceanviewMiddle', 'oceanviewAft', 'InteriorForward', 'InteriorMiddle', 'InteriorAft', 'oceanviewRoomsCost', 'InteriorRoomsCost']


class CruiseDetailFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CruiseDetailFinal
        fields = '__all__'

    def validate(self, data):
        if data['endDate'] <= data['startDate']:
            raise serializers.ValidationError("End date must be after start date")
        if data['oceanviewForward'] + data['oceanviewMiddle'] + data['oceanviewAft'] != data['oceanviewRooms']:
            raise serializers.ValidationError("Oceanview room counts do not match")
        if data['InteriorForward'] + data['InteriorMiddle'] + data['InteriorAft'] != data['InteriorRooms']:
            raise serializers.ValidationError("Interior room counts do not match")
        return data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        if Booking.objects.filter(
            cruise=data['cruise'],
            room_number=data['room_number']
        ).exists():
            raise serializers.ValidationError("This room is already booked")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


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
        user = LogedInUser(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user