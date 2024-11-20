# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from .models import Student,Cruise,CruiseDetail,CruiseDetailFinal, Booking,LogedInUser
from .serializers import StudentSerializer,CruiseSerializer,CruiseDetailSerializer,CruiseDetailFinalSerializer,BookingSerializer,LogedInUserSerializer
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging
from django.contrib.auth.hashers import check_password

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

class CruiseDetailFinalList(ListAPIView):
    queryset = CruiseDetailFinal.objects.all()  # This should be a valid queryset
    serializer_class = CruiseDetailFinalSerializer

# def get_rooms(request, cruise_id):
#     cruise = CruiseDetailFinal.objects.get(id=cruise_id)
#     booked_rooms = Booking.objects.filter(cruise=cruise).values_list('room_number', flat=True)
#     rooms = [f'B{i+1}' for i in range(cruise.oceanviewForward)]
    
#     data = {
#         'rooms': rooms,
#         'booked_rooms': list(booked_rooms),
#     }
    
#     return JsonResponse(data)

class CreateBooking(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# @api_view(['GET'])
# def booked_rooms(request, cruise_id):
#     cruise = CruiseDetailFinal.objects.get(id=cruise_id)
#     bookings = Booking.objects.filter(cruise=cruise)
#     serializer = BookingSerializer(bookings, many=True)
#     return Response(serializer.data)


# class CruiseDetailsDoneList(ListAPIView):
#     queryset = CruiseDetailsDone.objects.all()  # This should be a valid queryset
#     serializer_class = CruiseDetailsDoneSerializer


# class AvailableRoomsView(generics.ListAPIView):
#     serializer_class = CruiseDetailSerializer

#     def get_queryset(self):
#         room_type = self.request.query_params.get('roomType')
#         deck = self.request.query_params.get('deck')
#         location = self.request.query_params.get('location')
#         cruise_name = self.request.query_params.get('cruiseName')

#         queryset = CruiseDetailFinal.objects.filter(
#             cruiseName=cruise_name,
#             type=room_type,
#             decks=deck,
#             oceanviewForward=location if location == 'Forward' else None,
#             oceanviewMiddle=location if location == 'Middle' else None,
#             oceanviewAft=location if location == 'Aft' else None,
#             InteriorForward=location if location == 'Forward' else None,
#             InteriorMiddle=location if location == 'Middle' else None,
#             InteriorAft=location if location == 'Aft' else None,
#         )
#         return queryset

@login_required
def available_rooms(request, cruise_id, room_type):
    cruise = CruiseDetailFinal.objects.get(id=cruise_id)
    booked_rooms = Booking.objects.filter(cruise=cruise, room_type=room_type).values_list('room_number', flat=True)
    all_rooms = list(range(1, getattr(cruise, room_type) + 1))
    available_rooms = [room for room in all_rooms if room not in booked_rooms]
    return JsonResponse({'available_rooms': available_rooms})

@api_view(['POST'])
def book_room(request):
    permission_classes = [IsAuthenticated]
    data = request.data
    serializer = BookingSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Room booked successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_rooms(request, cruise_id, room_type, location):
    try:
        # Fetch the specific cruise
        cruise = CruiseDetailFinal.objects.get(id=cruise_id)

        # Get booked rooms based on cruise, room type, and location
        booked_rooms = Booking.objects.filter(
            cruise=cruise, room_type=room_type, location=location
        ).values_list('room_number', flat=True)

        # Construct field name dynamically based on room_type and location
        if room_type == 'Oceanview' and location == 'forward':
            field_name = 'oceanviewForward'
        elif room_type == 'Oceanview' and location == 'middle':
            field_name = 'oceanviewMiddle'
        elif room_type == 'Oceanview' and location == 'backward':
            field_name = 'oceanviewAft'
        elif room_type == 'Interior' and location == 'forward':
            field_name = 'InteriorForward'
        elif room_type == 'Interior' and location == 'middle':
            field_name = 'InteriorMiddle'
        elif room_type == 'Interior' and location == 'backward':
            field_name = 'InteriorAft'
        else:
            return JsonResponse({'error': 'Invalid room type or location'}, status=400)

        # Access the dynamically constructed field (e.g., oceanviewForward, InteriorMiddle)
        room_capacity = getattr(cruise, field_name)

        # Generate room numbers (e.g., B1, B2, B3, ..., B{room_capacity})
        available_rooms = [f'B{i+1}' for i in range(room_capacity)]
        
        # Remove already booked rooms from available rooms
        available_rooms = [room for room in available_rooms if room not in booked_rooms]

        return JsonResponse({
            'rooms': available_rooms,
            'booked_rooms': list(booked_rooms)
        })

    except CruiseDetailFinal.DoesNotExist:
        return JsonResponse({'error': 'Cruise not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['DELETE'])
def cancel_booking(request):
    permission_classes = [IsAuthenticated]
    cruise_id = request.data.get('cruise')
    room_type = request.data.get('room_type')
    booked_rooms = request.data.get('booked_rooms')

    # Log the received data
    print(f"Received data: cruise_id={cruise_id}, room_type={room_type}, booked_rooms={booked_rooms}")

    if not cruise_id or not room_type or not booked_rooms:
        return Response({"error": "Invalid data - missing cruise, room type, or booked rooms"}, status=400)

    if not booked_rooms:  # Additional check for empty booked_rooms
        return Response({"error": "No rooms provided for cancellation"}, status=400)

    try:
        # Proceed to delete the booking
        Booking.objects.filter(cruise_id=cruise_id, room_type=room_type, room_number__in=booked_rooms).delete()
        return Response({"message": "Rooms canceled successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    
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