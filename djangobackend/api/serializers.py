from rest_framework import serializers
from .models import (
    Student, Cruise, CruiseDetail, CruiseDetailFinal, Booking, LogedInUser,
    GuestProfile, Product, Package, PackageComponent, GroupBooking,
    BookingItinerary, OnboardSpending, Household, SalesforceIntegration
)

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


class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = '__all__'


class GuestProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestProfile
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        if data['type'] in ['DINING', 'CONFERENCE', 'SPA'] and not data.get('schedule'):
            raise serializers.ValidationError("Schedule is required for this product type")
        return data


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'

    def validate(self, data):
        if data['valid_to'] <= data['valid_from']:
            raise serializers.ValidationError("Valid to date must be after valid from date")
        return data


class GroupBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupBooking
        fields = '__all__'


class BookingItinerarySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = BookingItinerary
        fields = '__all__'

    def validate(self, data):
        if data['total_cost'] < 0:
            raise serializers.ValidationError("Total cost cannot be negative")
        return data


class OnboardSpendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardSpending
        fields = '__all__'


class SalesforceIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesforceIntegration
        fields = '__all__'