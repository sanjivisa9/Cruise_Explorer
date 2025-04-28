# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from .models import (
    Student, Cruise, CruiseDetail, CruiseDetailFinal, Booking,
    GuestProfile, Product, Package, GroupBooking, BookingItinerary,
    OnboardSpending, Household
)
from .serializers import (
    StudentSerializer, CruiseSerializer, CruiseDetailSerializer,
    CruiseDetailFinalSerializer, BookingSerializer, GuestProfileSerializer,
    ProductSerializer, PackageSerializer, GroupBookingSerializer,
    BookingItinerarySerializer, OnboardSpendingSerializer, HouseholdSerializer
)
from rest_framework import generics, status
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
import logging
from django.contrib.auth.hashers import check_password
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CruiseFilter
from .pagination import CustomPagination

logger = logging.getLogger(__name__)

class StudentList(ListAPIView):
    queryset = Student.objects.all()  # This should be a valid queryset
    serializer_class = StudentSerializer


class CruiseList(ListAPIView):
    queryset = Cruise.objects.all()  # This should be a valid queryset
    serializer_class = CruiseSerializer


class CruiseDetailList(ListAPIView):
    queryset = CruiseDetail.objects.all()  # This should be a valid queryset
    serializer_class = CruiseDetailSerializer


class CruiseDetailFinalList(generics.ListAPIView):
    queryset = CruiseDetailFinal.objects.all()
    serializer_class = CruiseDetailFinalSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CruiseFilter

    def get_queryset(self):
        queryset = CruiseDetailFinal.objects.all()
        origin = self.request.query_params.get('origin', None)
        if origin:
            queryset = queryset.filter(origin=origin)
        return queryset.select_related()


@login_required
def available_rooms(request, cruise_id, room_type):
    cruise = CruiseDetailFinal.objects.get(id=cruise_id)
    booked_rooms = Booking.objects.filter(cruise=cruise, room_type=room_type).values_list('room_number', flat=True)
    all_rooms = list(range(1, getattr(cruise, room_type) + 1))
    available_rooms = [room for room in all_rooms if room not in booked_rooms]
    return JsonResponse({'available_rooms': available_rooms})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_rooms(request, cruise_id, room_type, location):
    try:
        cruise = get_object_or_404(CruiseDetailFinal, id=cruise_id)
        
        # Get booked rooms
        booked_rooms = Booking.objects.filter(
            cruise=cruise,
            room_type=room_type,
            location=location
        ).values_list('room_number', flat=True)
        
        # Get total rooms based on type and location
        field_name = f"{room_type.lower()}{location.capitalize()}"
        total_rooms = getattr(cruise, field_name, 0)
        
        # Generate available room numbers
        all_rooms = [f'B{i+1}' for i in range(total_rooms)]
        available_rooms = [room for room in all_rooms if room not in booked_rooms]
        
        return Response({
            'available_rooms': available_rooms,
            'booked_rooms': list(booked_rooms)
        })
    except Exception as e:
        logger.error(f"Error in get_rooms: {str(e)}")
        return Response(
            {'error': 'Failed to fetch rooms'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class CreateBooking(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # Check if room is already booked
            existing_booking = Booking.objects.filter(
                cruise_id=request.data['cruise'],
                room_number=request.data['room_number']
            ).exists()
            
            if existing_booking:
                return Response(
                    {'error': 'Room already booked'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            return Response(
                {'message': 'Booking created successfully'},
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in CreateBooking: {str(e)}")
            return Response(
                {'error': 'Failed to create booking'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_booking(request):
    try:
        booking = get_object_or_404(
            Booking,
            cruise_id=request.data['cruise'],
            room_number=request.data['room_number'],
            user=request.user
        )
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error in cancel_booking: {str(e)}")
        return Response(
            {'error': 'Failed to cancel booking'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = LogedInUser.objects.get(email=email)
            if check_password(password, user.password):
                # Return success message
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        except LogedInUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class SignupView(APIView):
    def post(self, request):
        serializer = LogedInUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                return Response(status=204)
            else:
                return Response({"error": "No refresh token provided."}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ConfirmBooking(APIView):
    def post(self, request):
        # Add logic to confirm the booking here
        return Response({"message": "Booking confirmed successfully"}, status=status.HTTP_200_OK)


class HouseholdViewSet(generics.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        household = serializer.save()
        guest_profile = GuestProfile.objects.get(user=self.request.user)
        household.primary_contact = guest_profile
        household.save()


class GuestProfileViewSet(generics.ModelViewSet):
    queryset = GuestProfile.objects.all()
    serializer_class = GuestProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nationality', 'household']

    def get_queryset(self):
        if self.request.user.is_staff:
            return GuestProfile.objects.all()
        return GuestProfile.objects.filter(user=self.request.user)


class ProductViewSet(generics.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'is_allotment']


class PackageViewSet(generics.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['valid_from', 'valid_to']


class GroupBookingViewSet(generics.ModelViewSet):
    queryset = GroupBooking.objects.all()
    serializer_class = GroupBookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user.guestprofile)


class BookingItineraryViewSet(generics.ModelViewSet):
    queryset = BookingItinerary.objects.all()
    serializer_class = BookingItinerarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return BookingItinerary.objects.all()
        return BookingItinerary.objects.filter(guest__user=self.request.user)


class OnboardSpendingViewSet(generics.ModelViewSet):
    queryset = OnboardSpending.objects.all()
    serializer_class = OnboardSpendingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return OnboardSpending.objects.all()
        return OnboardSpending.objects.filter(guest__user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def guest_spending_history(request, guest_id):
    try:
        spending = OnboardSpending.objects.filter(guest_id=guest_id)
        serializer = OnboardSpendingSerializer(spending, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refer_guest(request):
    try:
        referrer = request.user.guestprofile
        referred_email = request.data.get('email')
        referral_code = request.data.get('referral_code')
        
        if GuestProfile.objects.filter(referral_code=referral_code).exists():
            return Response({'error': 'Invalid referral code'}, status=400)
            
        # Add referral logic here
        referrer.loyalty_points += 100  # Example points
        referrer.save()
        
        return Response({'message': 'Referral successful'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suggest_products(request):
    try:
        guest = request.user.guestprofile
        preferences = guest.onboard_preferences
        
        # Simple product suggestion based on preferences
        suggested_products = Product.objects.filter(
            type__in=preferences.get('interested_categories', [])
        )
        
        serializer = ProductSerializer(suggested_products, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)